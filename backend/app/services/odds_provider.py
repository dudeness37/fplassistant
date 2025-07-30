"""
The Odds API Provider - handles all interactions with The Odds API
"""
import os
import requests
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)

class OddsProvider:
    """
    Handles all The Odds API interactions with rate limiting and error handling
    """
    
    def __init__(self):
        self.api_key = os.getenv("ODDS_API_KEY")
        if not self.api_key:
            raise ValueError("ODDS_API_KEY environment variable is required")
        
        self.base_url = "https://api.the-odds-api.com/v4/sports"
        self.rate_limit = int(os.getenv("ODDS_API_REQUESTS_PER_MINUTE", "500"))
        self.last_request_time = 0
        self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            'User-Agent': 'FPL-Assistant/1.0',
            'Accept': 'application/json',
        })
    
    def _rate_limit_wait(self):
        """Ensure we don't exceed rate limits"""
        time_since_last = time.time() - self.last_request_time
        min_interval = 60 / self.rate_limit  # seconds between requests
        
        if time_since_last < min_interval:
            wait_time = min_interval - time_since_last
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make a request to The Odds API with error handling"""
        self._rate_limit_wait()
        
        if params is None:
            params = {}
        
        params['apiKey'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Odds API request successful: {endpoint}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Odds API request failed for {endpoint}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Invalid JSON response from {endpoint}: {e}")
            raise
    
    def get_sports(self) -> List[dict]:
        """Get all available sports"""
        logger.info("Fetching available sports...")
        return self._make_request("")
    
    def get_soccer_odds(self, region: str = "uk", markets: str = "h2h,totals,btts") -> List[dict]:
        """
        Get soccer odds for Premier League
        
        Args:
            region: Region for odds (uk, us, au, eu)
            markets: Comma-separated markets (h2h, totals, btts, spreads)
        """
        logger.info(f"Fetching soccer odds for markets: {markets}")
        
        params = {
            'regions': region,
            'markets': markets,
            'oddsFormat': 'decimal',
            'dateFormat': 'iso',
        }
        
        return self._make_request("soccer_epl/odds", params)
    
    def get_historical_odds(self, commence_time_from: str, commence_time_to: str = None) -> List[dict]:
        """
        Get historical odds for a date range
        
        Args:
            commence_time_from: Start time (ISO format)
            commence_time_to: End time (ISO format)
        """
        logger.info(f"Fetching historical odds from {commence_time_from}")
        
        params = {
            'regions': 'uk',
            'markets': 'h2h,totals,btts',
            'oddsFormat': 'decimal',
            'dateFormat': 'iso',
            'commenceTimeFrom': commence_time_from,
        }
        
        if commence_time_to:
            params['commenceTimeTo'] = commence_time_to
        
        return self._make_request("soccer_epl/odds-history", params)
    
    def get_player_props(self, event_id: str = None) -> List[dict]:
        """
        Get player proposition odds (anytime scorer, assists, etc.)
        Note: Not all bookmakers offer these markets
        """
        logger.info("Fetching player proposition odds...")
        
        params = {
            'regions': 'uk',
            'markets': 'player_anytime_td,player_assists',  # td = touchdown/score
            'oddsFormat': 'decimal',
            'dateFormat': 'iso',
        }
        
        endpoint = "soccer_epl/odds"
        if event_id:
            endpoint = f"soccer_epl/events/{event_id}/odds"
        
        return self._make_request(endpoint, params)


class OddsDataProcessor:
    """
    Processes raw Odds API data into our database format and calculates probabilities
    """
    
    @staticmethod
    def decimal_to_probability(odds: float) -> float:
        """Convert decimal odds to implied probability"""
        if odds <= 1.0:
            return 0.0
        return 1.0 / odds
    
    @staticmethod
    def calculate_poisson_params(home_odds: float, away_odds: float, draw_odds: float) -> Dict[str, float]:
        """
        Calculate Poisson parameters from match odds
        
        Returns:
            Dict with home_lambda, away_lambda, and expected goals
        """
        try:
            # Convert to probabilities
            prob_home = OddsDataProcessor.decimal_to_probability(home_odds)
            prob_away = OddsDataProcessor.decimal_to_probability(away_odds)
            prob_draw = OddsDataProcessor.decimal_to_probability(draw_odds)
            
            # Normalize probabilities (remove bookmaker margin)
            total_prob = prob_home + prob_away + prob_draw
            prob_home /= total_prob
            prob_away /= total_prob
            prob_draw /= total_prob
            
            # Estimate average goals using empirical relationships
            # These are approximations based on historical data
            avg_goals = 2.7  # Premier League average
            
            # Use draw probability to estimate goal variance
            # Higher draw probability suggests lower-scoring game
            goal_adjustment = 1.0 - (prob_draw - 0.25) * 2  # Baseline draw prob ~25%
            estimated_total_goals = avg_goals * max(0.5, goal_adjustment)
            
            # Split between teams based on win probabilities
            home_advantage = 0.3  # Typical home advantage
            home_strength = prob_home / (prob_home + prob_away)
            
            home_lambda = estimated_total_goals * (home_strength + home_advantage/2)
            away_lambda = estimated_total_goals * ((1 - home_strength) - home_advantage/2)
            
            return {
                "home_lambda": max(0.1, home_lambda),
                "away_lambda": max(0.1, away_lambda),
                "estimated_total_goals": estimated_total_goals,
                "prob_home": prob_home,
                "prob_away": prob_away,
                "prob_draw": prob_draw,
            }
            
        except (ValueError, ZeroDivisionError) as e:
            logger.warning(f"Failed to calculate Poisson params: {e}")
            return {
                "home_lambda": 1.5,
                "away_lambda": 1.2,
                "estimated_total_goals": 2.7,
                "prob_home": 0.45,
                "prob_away": 0.30,
                "prob_draw": 0.25,
            }
    
    @staticmethod
    def calculate_clean_sheet_probability(defending_lambda: float) -> float:
        """Calculate clean sheet probability using Poisson distribution"""
        try:
            # P(0 goals) = e^(-λ) * λ^0 / 0! = e^(-λ)
            return math.exp(-defending_lambda)
        except (ValueError, OverflowError):
            return 0.1  # Default low probability
    
    @staticmethod
    def process_match_odds(odds_data: List[dict]) -> List[dict]:
        """Process match odds data from The Odds API"""
        processed_odds = []
        
        for event in odds_data:
            event_id = event.get("id")
            commence_time = event.get("commence_time")
            home_team = event.get("home_team")
            away_team = event.get("away_team")
            
            # Process each bookmaker's odds
            for bookmaker in event.get("bookmakers", []):
                bookmaker_name = bookmaker.get("key")
                
                # Extract odds for different markets
                odds_record = {
                    "event_id": event_id,
                    "commence_time": commence_time,
                    "home_team": home_team,
                    "away_team": away_team,
                    "bookmaker": bookmaker_name,
                    "snapshot_time": datetime.utcnow().isoformat(),
                }
                
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key")
                    
                    if market_key == "h2h":
                        # Head-to-head market (1X2)
                        for outcome in market.get("outcomes", []):
                            outcome_name = outcome.get("name")
                            odds_value = outcome.get("price")
                            
                            if outcome_name == home_team:
                                odds_record["home_win"] = odds_value
                            elif outcome_name == away_team:
                                odds_record["away_win"] = odds_value
                            elif outcome_name == "Draw":
                                odds_record["draw"] = odds_value
                    
                    elif market_key == "totals":
                        # Over/Under goals market
                        for outcome in market.get("outcomes", []):
                            outcome_name = outcome.get("name")
                            odds_value = outcome.get("price")
                            point = outcome.get("point", 2.5)
                            
                            if outcome_name == "Over" and point == 2.5:
                                odds_record["over_2_5"] = odds_value
                            elif outcome_name == "Under" and point == 2.5:
                                odds_record["under_2_5"] = odds_value
                            elif outcome_name == "Over" and point == 1.5:
                                odds_record["over_1_5"] = odds_value
                            elif outcome_name == "Under" and point == 1.5:
                                odds_record["under_1_5"] = odds_value
                    
                    elif market_key == "btts":
                        # Both teams to score
                        for outcome in market.get("outcomes", []):
                            outcome_name = outcome.get("name")
                            odds_value = outcome.get("price")
                            
                            if outcome_name == "Yes":
                                odds_record["btts_yes"] = odds_value
                            elif outcome_name == "No":
                                odds_record["btts_no"] = odds_value
                
                # Calculate Poisson parameters if we have h2h odds
                if all(k in odds_record for k in ["home_win", "away_win", "draw"]):
                    poisson_params = OddsDataProcessor.calculate_poisson_params(
                        odds_record["home_win"],
                        odds_record["away_win"],
                        odds_record["draw"]
                    )
                    odds_record.update(poisson_params)
                    
                    # Calculate clean sheet probabilities
                    odds_record["home_clean_sheet_prob"] = OddsDataProcessor.calculate_clean_sheet_probability(
                        poisson_params["away_lambda"]
                    )
                    odds_record["away_clean_sheet_prob"] = OddsDataProcessor.calculate_clean_sheet_probability(
                        poisson_params["home_lambda"]
                    )
                
                processed_odds.append(odds_record)
        
        logger.info(f"Processed odds for {len(odds_data)} events from {len(set(o['bookmaker'] for o in processed_odds))} bookmakers")
        return processed_odds
    
    @staticmethod
    def process_player_odds(odds_data: List[dict]) -> List[dict]:
        """Process player proposition odds"""
        processed_odds = []
        
        for event in odds_data:
            event_id = event.get("id")
            
            for bookmaker in event.get("bookmakers", []):
                bookmaker_name = bookmaker.get("key")
                
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key")
                    
                    if market_key == "player_anytime_td":  # Anytime scorer
                        for outcome in market.get("outcomes", []):
                            player_name = outcome.get("name")
                            odds_value = outcome.get("price")
                            
                            odds_record = {
                                "event_id": event_id,
                                "player_name": player_name,
                                "bookmaker": bookmaker_name,
                                "anytime_scorer": odds_value,
                                "snapshot_time": datetime.utcnow().isoformat(),
                            }
                            processed_odds.append(odds_record)
        
        logger.info(f"Processed player odds for {len(processed_odds)} player-bookmaker combinations")
        return processed_odds