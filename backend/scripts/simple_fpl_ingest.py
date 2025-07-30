"""
Simple FPL data ingestion to get started quickly
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../infra/.env')

# Add app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from db.database import get_db, DatabaseManager, get_table_counts
import models
import requests
import logging
from datetime import datetime

# Get model classes
Team = models.Team
Player = models.Player
Fixture = models.Fixture
PlayerGameweekStats = models.PlayerGameweekStats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleFPLIngester:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.db_manager = DatabaseManager()
    
    def fetch_bootstrap_data(self):
        """Get the main FPL data"""
        logger.info("Fetching FPL bootstrap data...")
        try:
            response = self.session.get(f"{self.base_url}/bootstrap-static/", timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"✅ Bootstrap data fetched successfully")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch bootstrap data: {e}")
            raise
    
    def fetch_fixtures(self):
        """Get fixtures data"""
        logger.info("Fetching FPL fixtures...")
        try:
            response = self.session.get(f"{self.base_url}/fixtures/", timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"✅ Fixtures data fetched successfully")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch fixtures: {e}")
            raise
    
    def ingest_teams(self, bootstrap_data):
        """Ingest teams data"""
        db = next(get_db())
        try:
            teams_data = bootstrap_data.get("teams", [])
            logger.info(f"Processing {len(teams_data)} teams...")
            
            created_count = 0
            updated_count = 0
            
            for team_data in teams_data:
                team_record = {
                    "fpl_id": team_data["id"],
                    "name": team_data["name"],
                    "short_name": team_data["short_name"],
                    "league": "Premier League"
                }
                
                # Check if team exists
                existing = db.query(Team).filter(Team.fpl_id == team_data["id"]).first()
                if existing:
                    for key, value in team_record.items():
                        setattr(existing, key, value)
                    updated_count += 1
                else:
                    new_team = Team(**team_record)
                    db.add(new_team)
                    created_count += 1
            
            db.commit()
            logger.info(f"✅ Teams processed: {created_count} created, {updated_count} updated")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ingest teams: {e}")
            raise
        finally:
            db.close()
    
    def ingest_players(self, bootstrap_data):
        """Ingest players data"""
        db = next(get_db())
        try:
            players_data = bootstrap_data.get("elements", [])
            logger.info(f"Processing {len(players_data)} players...")
            
            # Create team mapping
            teams = {team.fpl_id: team.id for team in db.query(Team).all()}
            logger.info(f"Created mapping for {len(teams)} teams")
            
            # Position mapping
            position_map = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}
            
            created_count = 0
            updated_count = 0
            
            for player_data in players_data:
                team_id = teams.get(player_data["team"])
                if not team_id:
                    logger.warning(f"Could not find team for player {player_data['web_name']} (team_id: {player_data['team']})")
                    continue
                
                player_record = {
                    "fpl_id": player_data["id"],
                    "first_name": player_data["first_name"],
                    "second_name": player_data["second_name"],
                    "web_name": player_data["web_name"],
                    "team_id": team_id,
                    "position": position_map.get(player_data["element_type"], "Unknown"),
                    "price": float(player_data["now_cost"]) / 10,  # Convert from pence to pounds
                    "selected_by_percent": float(player_data["selected_by_percent"]),
                    "status": player_data["status"]
                }
                
                # Check if player exists
                existing = db.query(Player).filter(Player.fpl_id == player_data["id"]).first()
                if existing:
                    for key, value in player_record.items():
                        setattr(existing, key, value)
                    updated_count += 1
                else:
                    new_player = Player(**player_record)
                    db.add(new_player)
                    created_count += 1
            
            db.commit()
            logger.info(f"✅ Players processed: {created_count} created, {updated_count} updated")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ingest players: {e}")
            raise
        finally:
            db.close()
    
    def ingest_fixtures(self):
        """Ingest fixtures data"""
        db = next(get_db())
        try:
            fixtures_data = self.fetch_fixtures()
            logger.info(f"Processing {len(fixtures_data)} fixtures...")
            
            # Create team mapping
            teams = {team.fpl_id: team.id for team in db.query(Team).all()}
            
            created_count = 0
            updated_count = 0
            skipped_count = 0
            
            for fixture_data in fixtures_data:
                # Skip fixtures without kickoff time
                if not fixture_data.get("kickoff_time"):
                    skipped_count += 1
                    continue
                
                home_team_id = teams.get(fixture_data["team_h"])
                away_team_id = teams.get(fixture_data["team_a"])
                
                if not home_team_id or not away_team_id:
                    logger.warning(f"Could not find teams for fixture {fixture_data['id']}")
                    skipped_count += 1
                    continue
                
                try:
                    kickoff_time = datetime.fromisoformat(
                        fixture_data["kickoff_time"].replace('Z', '+00:00')
                    )
                except:
                    logger.warning(f"Invalid kickoff time for fixture {fixture_data['id']}")
                    skipped_count += 1
                    continue
                
                fixture_record = {
                    "fpl_id": fixture_data["id"],
                    "season": "2024-25",
                    "gameweek": fixture_data["event"],
                    "home_team_id": home_team_id,
                    "away_team_id": away_team_id,
                    "kickoff_time": kickoff_time,
                    "status": "finished" if fixture_data["finished"] else "scheduled"
                }
                
                # Add results if finished
                if fixture_data["finished"]:
                    fixture_record.update({
                        "home_score": fixture_data.get("team_h_score"),
                        "away_score": fixture_data.get("team_a_score")
                    })
                
                # Check if fixture exists
                existing = db.query(Fixture).filter(Fixture.fpl_id == fixture_data["id"]).first()
                if existing:
                    for key, value in fixture_record.items():
                        setattr(existing, key, value)
                    updated_count += 1
                else:
                    new_fixture = Fixture(**fixture_record)
                    db.add(new_fixture)
                    created_count += 1
            
            db.commit()
            logger.info(f"✅ Fixtures processed: {created_count} created, {updated_count} updated, {skipped_count} skipped")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to ingest fixtures: {e}")
            raise
        finally:
            db.close()
    
    def show_final_status(self):
        """Show final database status"""
        logger.info("\n" + "="*50)
        logger.info("📊 FINAL DATABASE STATUS")
        logger.info("="*50)
        
        counts = get_table_counts()
        for table, count in counts.items():
            if not str(count).startswith("Error") and count > 0:
                logger.info(f"{table:25} {count:>10}")
        
        logger.info("="*50)
    
    def run(self):
        """Run the full ingestion"""
        try:
            logger.info("🚀 Starting FPL data ingestion...")
            
            # Test database connection first
            from db.database import test_connection
            if not test_connection():
                raise Exception("Database connection failed")
            
            # Get bootstrap data
            bootstrap_data = self.fetch_bootstrap_data()
            
            # Ingest data in order
            self.ingest_teams(bootstrap_data)
            self.ingest_players(bootstrap_data)
            self.ingest_fixtures()
            
            # Show final status
            self.show_final_status()
            
            logger.info("🎉 FPL data ingestion completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ingestion failed: {e}")
            return False

def main():
    """Main entry point"""
    logger.info("FPL Assistant - Simple Data Ingestion")
    
    ingester = SimpleFPLIngester()
    success = ingester.run()
    
    if success:
        logger.info("✅ Data ingestion completed successfully!")
        exit(0)
    else:
        logger.error("❌ Data ingestion failed!")
        exit(1)

if __name__ == "__main__":
    main()