"""
Working Sportmonks data ingestion - adapted to your API plan
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../infra/.env')

# Add app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from db.database import get_db, get_table_counts
import models
import requests
import logging
from datetime import datetime

# Get model classes
Team = models.Team
MatchStatistics = models.MatchStatistics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkingSportmonksIngester:
    def __init__(self):
        self.api_key = os.getenv("SPORTMONKS_API_KEY")
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FPL-Assistant/1.0',
            'Accept': 'application/json',
        })
        
        logger.info("Sportmonks provider initialized")
    
    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make request to Sportmonks API"""
        if params is None:
            params = {}
        
        params['api_token'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API request failed for {endpoint}: {e}")
            raise
    
    def find_premier_league_season(self):
        """Find current Premier League season"""
        logger.info("Finding Premier League season...")
        
        # Get seasons and find Premier League (league_id = 8)
        seasons_data = self._make_request("seasons")
        seasons = seasons_data.get("data", [])
        
        # Find current season for Premier League
        current_season = None
        for season in seasons:
            if (season.get("league_id") == 8 and 
                "2024" in season.get("name", "")):
                current_season = season
                break
        
        if not current_season:
            # Get most recent PL season
            pl_seasons = [s for s in seasons if s.get("league_id") == 8]
            if pl_seasons:
                current_season = sorted(pl_seasons, key=lambda x: x.get("id", 0), reverse=True)[0]
        
        if current_season:
            logger.info(f"Found season: {current_season.get('name')} (ID: {current_season.get('id')})")
            return current_season
        else:
            logger.warning("Could not find Premier League season")
            return None
    
    def get_premier_league_teams(self):
        """Get Premier League teams"""
        logger.info("Fetching Premier League teams...")
        
        # Get all teams and filter for Premier League
        teams_data = self._make_request("teams")
        all_teams = teams_data.get("data", [])
        
        # Filter teams (we'll identify PL teams by matching names)
        pl_team_names = [
            "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
            "Chelsea", "Crystal Palace", "Everton", "Fulham", "Ipswich Town",
            "Leicester City", "Liverpool", "Manchester City", "Manchester United",
            "Newcastle United", "Nottingham Forest", "Southampton", "Tottenham",
            "West Ham United", "Wolverhampton Wanderers"
        ]
        
        pl_teams = []
        for team in all_teams:
            team_name = team.get("name", "")
            if any(pl_name in team_name for pl_name in pl_team_names):
                pl_teams.append(team)
        
        logger.info(f"Found {len(pl_teams)} Premier League teams")
        return pl_teams
    
    def get_recent_fixtures(self, limit: int = 100):
        """Get recent fixtures with potential PL matches"""
        logger.info("Fetching recent fixtures...")
        
        fixtures_data = self._make_request("fixtures", {"per_page": limit})
        fixtures = fixtures_data.get("data", [])
        
        # Filter for finished fixtures (we want matches with results)
        finished_fixtures = [
            f for f in fixtures 
            if f.get("state", {}).get("state") == "finished"
        ]
        
        logger.info(f"Found {len(finished_fixtures)} finished fixtures")
        return finished_fixtures
    
    def map_teams_to_sportmonks(self, sportmonks_teams):
        """Map FPL teams to Sportmonks teams"""
        db = next(get_db())
        
        try:
            # Create name mapping
            team_mapping = {}
            
            # Enhanced name mapping for better matches
            name_variations = {
                "Arsenal": ["Arsenal", "Arsenal FC"],
                "Aston Villa": ["Aston Villa", "Aston Villa FC"],
                "Bournemouth": ["Bournemouth", "AFC Bournemouth", "Bournemouth FC"],
                "Brentford": ["Brentford", "Brentford FC"],
                "Brighton": ["Brighton", "Brighton & Hove Albion", "Brighton and Hove Albion"],
                "Chelsea": ["Chelsea", "Chelsea FC"],
                "Crystal Palace": ["Crystal Palace", "Crystal Palace FC"],
                "Everton": ["Everton", "Everton FC"],
                "Fulham": ["Fulham", "Fulham FC"],
                "Ipswich": ["Ipswich", "Ipswich Town", "Ipswich Town FC"],
                "Leicester": ["Leicester", "Leicester City", "Leicester City FC"],
                "Liverpool": ["Liverpool", "Liverpool FC"],
                "Man City": ["Manchester City", "Manchester City FC"],
                "Man Utd": ["Manchester United", "Manchester United FC"],
                "Newcastle": ["Newcastle", "Newcastle United", "Newcastle United FC"],
                "Nott'm Forest": ["Nottingham Forest", "Nottingham Forest FC"],
                "Southampton": ["Southampton", "Southampton FC"],
                "Spurs": ["Tottenham", "Tottenham Hotspur", "Tottenham Hotspur FC"],
                "West Ham": ["West Ham", "West Ham United", "West Ham United FC"],
                "Wolves": ["Wolves", "Wolverhampton Wanderers", "Wolverhampton Wanderers FC"]
            }
            
            # Map Sportmonks teams to FPL names
            for sportmonks_team in sportmonks_teams:
                sportmonks_name = sportmonks_team.get("name", "")
                sportmonks_id = sportmonks_team.get("id")
                
                for fpl_name, variations in name_variations.items():
                    if any(var in sportmonks_name for var in variations):
                        team_mapping[fpl_name] = {
                            "sportmonks_id": sportmonks_id,
                            "sportmonks_name": sportmonks_name
                        }
                        break
            
            # Update FPL teams
            updated_count = 0
            for fpl_team in db.query(Team).all():
                if fpl_team.short_name in team_mapping:
                    mapping_info = team_mapping[fpl_team.short_name]
                    fpl_team.sportmonks_id = mapping_info["sportmonks_id"]
                    updated_count += 1
                    logger.info(f"Mapped {fpl_team.short_name} → {mapping_info['sportmonks_name']} (ID: {mapping_info['sportmonks_id']})")
            
            db.commit()
            logger.info(f"✅ Updated {updated_count} teams with Sportmonks IDs")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to map teams: {e}")
            raise
        finally:
            db.close()
    
    def extract_fixture_stats(self, fixtures):
        """Extract basic stats from fixtures"""
        logger.info("Processing fixture statistics...")
        
        db = next(get_db())
        team_mapping = {team.sportmonks_id: team.id for team in db.query(Team).filter(Team.sportmonks_id.isnot(None)).all()}
        db.close()
        
        stats_inserted = 0
        
        db = next(get_db())
        try:
            for fixture in fixtures:
                fixture_id = fixture.get("id")
                participants = fixture.get("participants", [])
                
                # Basic match info
                home_score = fixture.get("scores", [{}])[0].get("score", {}).get("goals") if fixture.get("scores") else None
                away_score = fixture.get("scores", [{}])[-1].get("score", {}).get("goals") if fixture.get("scores") and len(fixture.get("scores", [])) > 1 else None
                
                for participant in participants:
                    sportmonks_team_id = participant.get("id")
                    team_id = team_mapping.get(sportmonks_team_id)
                    
                    if not team_id:
                        continue
                    
                    is_home = participant.get("meta", {}).get("location") == "home"
                    
                    # Check if already exists
                    existing = db.query(MatchStatistics).filter(
                        MatchStatistics.fixture_sportmonks_id == fixture_id,
                        MatchStatistics.team_id == team_id
                    ).first()
                    
                    if existing:
                        continue
                    
                    # Create basic match statistic
                    match_stat = MatchStatistics(
                        fixture_sportmonks_id=fixture_id,
                        team_id=team_id,
                        is_home=is_home,
                        # We'll add basic data and enhance later when we get detailed stats
                        xg=0,  # Placeholder - will be updated when we get detailed stats
                        shots_total=0,
                        shots_on_target=0,
                        possession_percentage=0,
                        corners=0
                    )
                    
                    db.add(match_stat)
                    stats_inserted += 1
            
            db.commit()
            logger.info(f"✅ Inserted {stats_inserted} basic match statistics")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to process fixture stats: {e}")
            raise
        finally:
            db.close()
    
    def show_sample_data(self):
        """Show sample of what we've added"""
        db = next(get_db())
        
        try:
            logger.info("\n" + "="*50)
            logger.info("📊 SPORTMONKS DATA SAMPLE")
            logger.info("="*50)
            
            # Show teams with Sportmonks IDs
            teams_with_sportmonks = db.query(Team).filter(Team.sportmonks_id.isnot(None)).limit(5)
            logger.info("\n🏆 Teams mapped to Sportmonks:")
            for team in teams_with_sportmonks:
                logger.info(f"  {team.short_name} → Sportmonks ID: {team.sportmonks_id}")
            
            # Show match statistics
            stats_count = db.query(MatchStatistics).count()
            logger.info(f"\n⚽ Match statistics records: {stats_count}")
            
            if stats_count > 0:
                recent_stats = db.query(MatchStatistics).limit(3)
                for stat in recent_stats:
                    team = db.query(Team).filter(Team.id == stat.team_id).first()
                    logger.info(f"  {team.short_name}: Fixture {stat.fixture_sportmonks_id} ({'Home' if stat.is_home else 'Away'})")
            
        finally:
            db.close()
    
    def run(self):
        """Run the Sportmonks data enrichment"""
        try:
            logger.info("🚀 Starting Sportmonks data enrichment...")
            
            # Step 1: Find Premier League season
            season = self.find_premier_league_season()
            if not season:
                logger.warning("Could not find Premier League season, continuing anyway...")
            
            # Step 2: Get Premier League teams
            pl_teams = self.get_premier_league_teams()
            
            # Step 3: Map FPL teams to Sportmonks
            self.map_teams_to_sportmonks(pl_teams)
            
            # Step 4: Get recent fixtures and extract basic stats
            fixtures = self.get_recent_fixtures()
            self.extract_fixture_stats(fixtures)
            
            # Step 5: Show results
            self.show_sample_data()
            
            # Final status
            logger.info("\n📊 Final Database Status:")
            counts = get_table_counts()
            for table, count in counts.items():
                if not str(count).startswith("Error") and count > 0:
                    logger.info(f"{table:25} {count:>10}")
            
            logger.info("🎉 Sportmonks data enrichment completed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Enrichment failed: {e}")
            return False

def main():
    """Main entry point"""
    logger.info("FPL Assistant - Working Sportmonks Integration")
    
    try:
        ingester = WorkingSportmonksIngester()
        success = ingester.run()
        
        if success:
            logger.info("✅ Success! Your database now has Sportmonks team mappings!")
            logger.info("🔧 Next: We can add detailed xG data and build feature calculations!")
        else:
            logger.error("❌ Integration failed!")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}")

if __name__ == "__main__":
    main()