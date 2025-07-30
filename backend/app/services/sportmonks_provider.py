"""
Sportmonks API Provider - Enhanced data for feature calculations
"""

import os
import requests
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# Import dotenv FIRST, then use it
try:
    from dotenv import load_dotenv
    load_dotenv('../../infra/.env')
except ImportError:
    # dotenv not available, assume env vars are set by system
    pass

logger = logging.getLogger(__name__)

class SportmonksProvider:
    """
    Handles Sportmonks API interactions for xG data, lineups, and historical stats
    """
    
    def __init__(self):
        self.api_key = os.getenv("SPORTMONKS_API_KEY")
        if not self.api_key:
            raise ValueError("SPORTMONKS_API_KEY environment variable is required")
        
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.rate_limit = 60  # requests per minute
        self.last_request_time = 0
        self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            'User-Agent': 'FPL-Assistant/1.0',
            'Accept': 'application/json',
        })
        
        logger.info("Sportmonks provider initialized")
    
    def _rate_limit_wait(self):
        """Ensure we don't exceed rate limits"""
        time_since_last = time.time() - self.last_request_time
        min_interval = 60 / self.rate_limit  # seconds between requests
        
        if time_since_last < min_interval:
            wait_time = min_interval - time_since_last
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make a request to Sportmonks API with error handling"""
        self._rate_limit_wait()
        
        if params is None:
            params = {}
        
        params['api_token'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Sportmonks API request successful: {endpoint}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Sportmonks API request failed for {endpoint}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Invalid JSON response from {endpoint}: {e}")
            raise
    
    def get_leagues(self) -> List[dict]:
        """Get all available leagues"""
        logger.info("Fetching Sportmonks leagues...")
        response = self._make_request("leagues")
        return response.get("data", [])
    
    def get_premier_league_id(self) -> int:
        """Get the Premier League ID from Sportmonks"""
        leagues = self.get_leagues()
        for league in leagues:
            if "Premier League" in league.get("name", "") and league.get("country_id") == 462:  # England
                logger.info(f"Found Premier League ID: {league['id']}")
                return league["id"]
        raise ValueError("Premier League not found in Sportmonks leagues")
    
    def get_current_season(self, league_id: int) -> dict:
        """Get current season for Premier League"""
        logger.info(f"Fetching current season for league {league_id}...")
        response = self._make_request(f"leagues/{league_id}/seasons")
        seasons = response.get("data", [])
        
        # Find current season (2024-2025)
        for season in seasons:
            if "2024" in season.get("name", ""):
                logger.info(f"Found current season: {season['name']} (ID: {season['id']})")
                return season
        
        # Fallback to most recent
        if seasons:
            current = sorted(seasons, key=lambda x: x.get("starting_at", ""), reverse=True)[0]
            logger.info(f"Using most recent season: {current['name']} (ID: {current['id']})")
            return current
        
        raise ValueError("No seasons found for Premier League")
    
    def get_teams(self, league_id: int, season_id: int) -> List[dict]:
        """Get teams for current Premier League season"""
        logger.info(f"Fetching teams for league {league_id}, season {season_id}")
        
        params = {
            'include': 'venue,players',
        }
        
        response = self._make_request(f"leagues/{league_id}/seasons/{season_id}/teams", params)
        return response.get("data", [])
    
    def get_fixtures_with_stats(self, league_id: int, season_id: int, limit: int = 50) -> List[dict]:
        """Get recent fixtures with statistics"""
        logger.info(f"Fetching recent fixtures with stats for league {league_id}")
        
        params = {
            'include': 'participants,statistics,events',
            'per_page': limit,
        }
        
        response = self._make_request(f"leagues/{league_id}/seasons/{season_id}/fixtures", params)
        fixtures = response.get("data", [])
        
        # Filter for finished matches with stats
        finished_fixtures = [f for f in fixtures if f.get("state", {}).get("state") == "finished"]
        
        logger.info(f"Found {len(finished_fixtures)} finished fixtures with stats")
        return finished_fixtures
    
    def get_player_season_stats(self, league_id: int, season_id: int) -> List[dict]:
        """Get player statistics for the season"""
        logger.info(f"Fetching player season stats for league {league_id}")
        
        params = {
            'include': 'player,team,details',
        }
        
        response = self._make_request(f"leagues/{league_id}/seasons/{season_id}/statistics/players", params)
        return response.get("data", [])

class SportmonksDataProcessor:
    """
    Processes Sportmonks data for our database
    """
    
    @staticmethod
    def process_team_mapping(teams_data: List[dict]) -> dict:
        """Create mapping between FPL team names and Sportmonks team IDs"""
        mapping = {}
        
        # Common name variations for mapping
        name_mappings = {
            "Arsenal": ["Arsenal", "Arsenal FC"],
            "Aston Villa": ["Aston Villa", "Aston Villa FC"],
            "Bournemouth": ["Bournemouth", "AFC Bournemouth", "Bournemouth FC"],
            "Brentford": ["Brentford", "Brentford FC"],
            "Brighton": ["Brighton", "Brighton & Hove Albion", "Brighton and Hove Albion FC"],
            "Chelsea": ["Chelsea", "Chelsea FC"],
            "Crystal Palace": ["Crystal Palace", "Crystal Palace FC"],
            "Everton": ["Everton", "Everton FC"],
            "Fulham": ["Fulham", "Fulham FC"],
            "Ipswich": ["Ipswich", "Ipswich Town", "Ipswich Town FC"],
            "Leicester": ["Leicester", "Leicester City", "Leicester City FC"],
            "Liverpool": ["Liverpool", "Liverpool FC"],
            "Man City": ["Manchester City", "Manchester City FC", "Man City"],
            "Man Utd": ["Manchester United", "Manchester United FC", "Man Utd"],
            "Newcastle": ["Newcastle", "Newcastle United", "Newcastle United FC"],
            "Nott'm Forest": ["Nottingham Forest", "Nottingham Forest FC", "Nott'm Forest"],
            "Southampton": ["Southampton", "Southampton FC"],
            "Spurs": ["Tottenham", "Tottenham Hotspur", "Tottenham Hotspur FC", "Spurs"],
            "West Ham": ["West Ham", "West Ham United", "West Ham United FC"],
            "Wolves": ["Wolves", "Wolverhampton Wanderers", "Wolverhampton Wanderers FC"]
        }
        
        for team_data in teams_data:
            team_name = team_data.get("name", "")
            team_id = team_data.get("id")
            
            # Find matching FPL team
            for fpl_name, variations in name_mappings.items():
                if team_name in variations:
                    mapping[fpl_name] = {
                        "sportmonks_id": team_id,
                        "name": team_name
                    }
                    break
        
        logger.info(f"Created team mapping for {len(mapping)} teams")
        return mapping
    
    @staticmethod
    def process_match_statistics(fixtures_data: List[dict]) -> List[dict]:
        """Process match statistics for xG data"""
        match_stats = []
        
        for fixture in fixtures_data:
            fixture_id = fixture.get("id")
            participants = fixture.get("participants", [])
            statistics = fixture.get("statistics", [])
            
            if not participants or not statistics:
                continue
            
            # Process each team's stats
            for participant in participants:
                team_id = participant.get("id")
                team_name = participant.get("name")
                is_home = participant.get("meta", {}).get("location") == "home"
                
                # Find stats for this team
                team_stats = None
                for stat in statistics:
                    if stat.get("participant_id") == team_id:
                        team_stats = stat
                        break
                
                if not team_stats:
                    continue
                
                # Extract key metrics
                stats_dict = {
                    "fixture_id": fixture_id,
                    "team_name": team_name,
                    "sportmonks_team_id": team_id,
                    "is_home": is_home,
                }
                
                # Parse statistics details
                details = team_stats.get("details", [])
                for detail in details:
                    stat_type = detail.get("type", {}).get("name", "").lower()
                    value = detail.get("value", 0)
                    
                    if "expected goals" in stat_type or "xg" in stat_type:
                        stats_dict["xg"] = float(value)
                    elif "shots" in stat_type and "total" in stat_type:
                        stats_dict["shots_total"] = int(value)
                    elif "shots on target" in stat_type:
                        stats_dict["shots_on_target"] = int(value)
                    elif "possession" in stat_type:
                        stats_dict["possession"] = float(value)
                    elif "corners" in stat_type:
                        stats_dict["corners"] = int(value)
                
                match_stats.append(stats_dict)
        
        logger.info(f"Processed statistics for {len(match_stats)} team performances")
        return match_stats

def test_sportmonks_connection():
    """Test Sportmonks API connection"""
    try:
        provider = SportmonksProvider()
        leagues = provider.get_leagues()
        logger.info(f"✅ Sportmonks connection successful - found {len(leagues)} leagues")
        
        # Try to find Premier League
        pl_id = provider.get_premier_league_id()
        logger.info(f"✅ Premier League found with ID: {pl_id}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Sportmonks connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    logging.basicConfig(level=logging.INFO)
    test_sportmonks_connection()