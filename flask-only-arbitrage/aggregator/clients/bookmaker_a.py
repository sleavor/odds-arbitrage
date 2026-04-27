import requests
from ..helpers import normalize_event

from config import ODDS_API_URL, ODDS_API_KEY

class BookmakerAClient:
    """Client for the-odds-api.com - returns odds from multiple bookmakers"""
    name = "TheOddsAPI"

    def __init__(self):
        if not ODDS_API_URL or not ODDS_API_KEY:
            raise RuntimeError("Odds API client not configured")
        self.base = ODDS_API_URL
        self.api_key = ODDS_API_KEY

    def fetch_odds(self, sport="baseball_mlb", region="us", mkt="totals"):
        """
        Fetch odds from the-odds-api.com
        
        Args:
            sport: Sport key (e.g., 'baseball_mlb', 'football_nfl')
            region: Region filter (e.g., 'us', 'uk', 'eu')
            mkt: Market type (e.g., 'h2h' for head-to-head, 'totals')
        
        Returns:
            List of events with odds from multiple bookmakers
        """
        url = f"{self.base}/odds/"
        params = {
            "apiKey": self.api_key,
            "sport": sport,
            "region": region,
            "mkt": mkt
        }
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        events_data = data.get("data", [])
        
        events = []
        for e in events_data:
            # Parse the sites array to extract odds per bookmaker
            markets = {}
            
            # Get teams from the event
            teams = e.get("teams", [])
            home_team = e.get("home_team", teams[0] if teams else "")
            away_team = e.get("away_team", teams[1] if len(teams) > 1 else "")
            
            # Iterate through ALL sites (bookmakers)
            for site in e.get("sites", []):
                site_nice = site.get("site_nice", site.get("site_key", "Unknown"))
                
                # Parse odds - they're stored as dict by market type
                site_odds = site.get("odds", {})
                
                for market_type, market_data in site_odds.items():
                    if market_type not in markets:
                        markets[market_type] = {}
                    
                    # Handle different market structures
                    if isinstance(market_data, dict):
                        # Check if it's the new format with position array
                        positions = market_data.get("position", [])
                        if positions:
                            # New format: { "position": [...], "odds": [...], "points": [...] }
                            odds_values = market_data.get("odds", [])
                            points = market_data.get("points", [])
                            
                            for i, position in enumerate(positions):
                                if i < len(odds_values):
                                    sel_name = position.capitalize()
                                    if market_type == "totals" and points:
                                        sel_name = f"{position.capitalize()} {points[i]}"
                                    
                                    if sel_name not in markets[market_type]:
                                        markets[market_type][sel_name] = []
                                    markets[market_type][sel_name].append({
                                        "odds": odds_values[i],
                                        "bookmaker": site_nice
                                    })
                        else:
                            # Spreads/totals format: { "odds": [...], "points": [...] }
                            odds_values = market_data.get("odds", [])
                            points = market_data.get("points", [])
                            
                            if market_type == "spreads" and len(odds_values) >= 2 and points:
                                # First point is for home team, second for away team
                                if home_team:
                                    sel_name = f"{home_team} ({points[0]})"
                                    if sel_name not in markets[market_type]:
                                        markets[market_type][sel_name] = []
                                    markets[market_type][sel_name].append({
                                        "odds": odds_values[0],
                                        "bookmaker": site_nice
                                    })
                                if away_team:
                                    sel_name = f"{away_team} ({points[1]})"
                                    if sel_name not in markets[market_type]:
                                        markets[market_type][sel_name] = []
                                    markets[market_type][sel_name].append({
                                        "odds": odds_values[1],
                                        "bookmaker": site_nice
                                    })
                            elif market_type == "totals" and len(odds_values) >= 2 and points:
                                # Totals: Over and Under
                                if len(points) >= 1:
                                    over_name = f"Over {points[0]}"
                                    under_name = f"Under {points[0]}"
                                    
                                    if over_name not in markets[market_type]:
                                        markets[market_type][over_name] = []
                                    markets[market_type][over_name].append({
                                        "odds": odds_values[0],
                                        "bookmaker": site_nice
                                    })
                                    
                                    if under_name not in markets[market_type]:
                                        markets[market_type][under_name] = []
                                    markets[market_type][under_name].append({
                                        "odds": odds_values[1],
                                        "bookmaker": site_nice
                                    })
                    
                    elif isinstance(market_data, list):
                        # h2h format: [home_odds, away_odds]
                        if market_type == "h2h" and len(market_data) >= 2:
                            if home_team:
                                if home_team not in markets[market_type]:
                                    markets[market_type][home_team] = []
                                markets[market_type][home_team].append({
                                    "odds": market_data[0],
                                    "bookmaker": site_nice
                                })
                            if away_team:
                                if away_team not in markets[market_type]:
                                    markets[market_type][away_team] = []
                                markets[market_type][away_team].append({
                                    "odds": market_data[1],
                                    "bookmaker": site_nice
                                })
            
            events.append({
                "source": self.name,
                "event_id": e.get("id"),
                "sport_key": e.get("sport_key"),
                "name": normalize_event(home_team + " vs " + away_team),
                "home_team": home_team,
                "away_team": away_team,
                "commence_time": e.get("commence_time"),
                "markets": markets
            })
        
        return events