"""
Main data ingestion script - orchestrates all data providers
Run this to populate your database with all necessary data
"""
import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from db.database import get_db, test_connection, get_table_counts, DatabaseManager
from services.fpl_provider import FPLProvider, FPLDataProcessor
from services.sportmonks_provider import SportmonksProvider, SportmonksDataProcessor
from services.odds_provider import OddsProvider, OddsDataProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataIngestionOrchestrator:
    """
    Orchestrates data ingestion from all providers
    """
    
    def __init__(self):
        self.fpl_provider = FPLProvider()
        self.sportmonks_provider = SportmonksProvider()
        self.odds_provider = OddsProvider()
        self.db_manager = DatabaseManager()
    
    def run_initial_setup(self):
        """
        Run the complete initial data setup
        This is for the first time setup - loads historical data
        """
        logger.info("🚀 Starting initial data ingestion setup...")
        
        # Test database connection
        if not test_connection():
            logger.error("❌ Database connection failed. Please check your DATABASE_URL")
            return False
        
        logger.info("✅ Database connection successful")
        
        try:
            # Phase 1: FPL Core Data
            logger.info("\n📊 Phase 1: Loading FPL core data...")
            self._ingest_fpl_data()
            
            # Phase 2: Sportmonks Historical Data
            logger.info("\n⚽ Phase 2: Loading Sportmonks historical data...")
            self._ingest_sportmonks_historical()
            
            # Phase 3: Odds Data
            logger.info("\n🎯 Phase 3: Loading odds data...")
            self._ingest_odds_data()
            
            # Final status
            self._print_final_status()
            
            logger.info("🎉 Initial data ingestion completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Data ingestion failed: {e}", exc_info=True)
            return False
    
    def _ingest_fpl_data(self):
        """Ingest FPL core data"""
        db = next(get_db())
        
        try:
            # Get bootstrap data
            logger.info("Fetching FPL bootstrap data...")
            bootstrap_data = self.fpl_provider.get_bootstrap_static()
            
            # Process and insert teams
            logger.info("Processing teams...")
            teams_data = FPLDataProcessor.process_teams(bootstrap_data)
            
            from app.models import Team  # Import your Team model
            
            for team_data in teams_data:
                self.db_manager.upsert_record(
                    db, Team, team_data, ['fpl_id']
                )
            
            logger.info(f"✅ Inserted/updated {len(teams_data)} teams")
            
            # Process and insert players
            logger.info("Processing players...")
            players_data = FPLDataProcessor.process_players(bootstrap_data)
            
            from app.models import Player  # Import your Player model
            
            # First, create a mapping of FPL team ID to our team ID
            teams_mapping = {}
            for team in db.query(Team).all():
                teams_mapping[team.fpl_id] = team.id
            
            for player_data in players_data:
                # Map FPL team ID to our team ID
                fpl_team_id = player_data.pop('fpl_team_id')
                player_data['team_id'] = teams_mapping.get(fpl_team_id)
                
                self.db_manager.upsert_record(
                    db, Player, player_data, ['fpl_id']
                )
            
            logger.info(f"✅ Inserted/updated {len(players_data)} players")
            
            # Process and insert fixtures
            logger.info("Processing fixtures...")
            fixtures_data = self.fpl_provider.get_fixtures()
            processed_fixtures = FPLDataProcessor.process_fixtures(fixtures_data)
            
            from app.models import Fixture  # Import your Fixture model
            
            for fixture_data in processed_fixtures:
                # Map team IDs
                home_fpl_id = fixture_data.pop('home_team_fpl_id')
                away_fpl_id = fixture_data.pop('away_team_fpl_id')
                fixture_data['home_team_id'] = teams_mapping.get(home_fpl_id)
                fixture_data['away_team_id'] = teams_mapping.get(away_fpl_id)
                
                self.db_manager.upsert_record(
                    db, Fixture, fixture_data, ['fpl_id']
                )
            
            logger.info(f"✅ Inserted/updated {len(processed_fixtures)} fixtures")
            
            # Process player gameweek history for key players (top 100 by ownership)
            logger.info("Processing player gameweek history...")
            
            # Get top players by ownership to start with
            top_players = sorted(players_data, key=lambda x: x.get('selected_by_percent', 0), reverse=True)[:100]
            
            from app.models import PlayerGameweekStats
            
            for i, player_data in enumerate(top_players):
                if i % 20 == 0:
                    logger.info(f"Processing player history {i+1}/{len(top_players)}")
                
                try:
                    player_summary = self.fpl_provider.get_player_summary(player_data['fpl_id'])
                    gameweeks = FPLDataProcessor.process_player_gameweek_history(
                        player_summary, player_data['fpl_id']
                    )
                    
                    # Map player ID
                    our_player_id = None
                    for player in db.query(Player).filter(Player.fpl_id == player_data['fpl_id']).first():
                        our_player_id = player.id
                        break
                    
                    for gw_data in gameweeks:
                        gw_data['player_id'] = our_player_id
                        gw_data.pop('fpl_player_id', None)
                        
                        self.db_manager.upsert_record(
                            db, PlayerGameweekStats, gw_data, ['player_id', 'season', 'gameweek']
                        )
                
                except Exception as e:
                    logger.warning(f"Failed to get history for player {player_data['fpl_id']}: {e}")
                    continue
            
            logger.info(f"✅ Processed gameweek history for {len(top_players)} players")
            
        except Exception as e:
            logger.error(f"FPL data ingestion failed: {e}")
            raise
        finally:
            db.close()
    
    def _ingest_sportmonks_historical(self):
        """Ingest historical data from Sportmonks"""
        db = next(get_db())
        
        try:
            # Get Premier League ID
            logger.info("Finding Premier League in Sportmonks...")
            pl_id = self.sportmonks_provider.get_premier_league_id()
            logger.info(f"Premier League ID: {pl_id}")
            
            # Get last 3 seasons
            seasons = self.sportmonks_provider.get_seasons(pl_id)
            recent_seasons = sorted(seasons, key=lambda x: x.get('name', ''), reverse=True)[:3]
            
            logger.info(f"Found {len(recent_seasons)} recent seasons")
            
            for season in recent_seasons:
                season_id = season['id']
                season_name = season.get('name', 'Unknown')
                logger.info(f"\n📅 Processing season: {season_name}")
                
                # Get teams for this season
                teams_data = self.sportmonks_provider.get_teams(pl_id, season_id)
                processed_teams = SportmonksDataProcessor.process_teams(teams_data)
                
                from app.models import Team
                
                # Update existing teams with Sportmonks IDs
                for team_data in processed_teams:
                    # Try to match by name
                    existing_team = db.query(Team).filter(
                        Team.name.ilike(f"%{team_data['name']}%")
                    ).first()
                    
                    if existing_team:
                        existing_team.sportmonks_id = team_data['sportmonks_id']
                        if not existing_team.venue:
                            existing_team.venue = team_data.get('venue')
                        if not existing_team.current_manager:
                            existing_team.current_manager = team_data.get('current_manager')
                        db.commit()
                
                logger.info(f"✅ Updated teams with Sportmonks data for {season_name}")
                
                # Get fixtures for this season (last 50 matches to avoid rate limits)
                fixtures_data = self.sportmonks_provider.get_fixtures(pl_id, season_id)
                recent_fixtures = fixtures_data[-50:] if len(fixtures_data) > 50 else fixtures_data
                
                from app.models import MatchStatistics
                
                for fixture in recent_fixtures:
                    try:
                        # Get detailed statistics for this fixture
                        detailed_fixture = self.sportmonks_provider.get_fixture_statistics(fixture['id'])
                        
                        # Process match statistics
                        match_stats = SportmonksDataProcessor.process_match_statistics(detailed_fixture)
                        
                        for stat_data in match_stats:
                            # Map Sportmonks team ID to our team ID
                            team = db.query(Team).filter(
                                Team.sportmonks_id == stat_data['team_sportmonks_id']
                            ).first()
                            
                            if team:
                                stat_data['team_id'] = team.id
                                stat_data['fixture_sportmonks_id'] = fixture['id']
                                
                                self.db_manager.upsert_record(
                                    db, MatchStatistics, stat_data, ['fixture_sportmonks_id', 'team_id']
                                )
                    
                    except Exception as e:
                        logger.warning(f"Failed to process fixture {fixture['id']}: {e}")
                        continue
                
                logger.info(f"✅ Processed {len(recent_fixtures)} fixtures for {season_name}")
        
        except Exception as e:
            logger.error(f"Sportmonks data ingestion failed: {e}")
            raise
        finally:
            db.close()
    
    def _ingest_odds_data(self):
        """Ingest odds data"""
        logger.info("Fetching current Premier League odds...")
        
        try:
            # Get current odds
            current_odds = self.odds_provider.get_soccer_odds()
            processed_odds = OddsDataProcessor.process_match_odds(current_odds)
            
            db = next(get_db())
            
            from app.models import MatchOdds
            
            for odds_data in processed_odds:
                # We'll need to map event IDs to our fixtures later
                # For now, just store the odds with the external event ID
                self.db_manager.upsert_record(
                    db, MatchOdds, odds_data, ['event_id', 'bookmaker']
                )
            
            logger.info(f"✅ Inserted/updated odds for {len(current_odds)} matches")
            
        except Exception as e:
            logger.error(f"Odds data ingestion failed: {e}")
            # Don't raise - odds are nice to have but not critical
        finally:
            db.close()
    
    def _print_final_status(self):
        """Print final status of data ingestion"""
        logger.info("\n📊 Final Database Status:")
        logger.info("=" * 50)
        
        counts = get_table_counts()
        for table, count in counts.items():
            logger.info(f"{table:25} {count:>10}")
        
        logger.info("=" * 50)

def main():
    """Main entry point"""
    logger.info("FPL Assistant - Data Ingestion Starting...")
    
    orchestrator = DataIngestionOrchestrator()
    success = orchestrator.run_initial_setup()
    
    if success:
        logger.info("✅ Data ingestion completed successfully!")
        exit(0)
    else:
        logger.error("❌ Data ingestion failed!")
        exit(1)

if __name__ == "__main__":
    main()