import os
from typing import List, Dict
from config import ODDS_API_KEY

# Local imports
from .clients.bookmaker_a import BookmakerAClient
from .helpers import normalize_event
class OddsAggregator:
    def __init__(self):
        self.clients = []
        if ODDS_API_KEY:
            try:
                self.clients.append(BookmakerAClient())
            except RuntimeError as e:
                print(f"[DEBUG] Failed to add BookmakerAClient: {e}")

    def aggregate(self, sport_key=None, region="us", mkt="totals") -> List[Dict]:
        """
        Returns list of events:
        {
          "name": "team a vs team b",
          "markets": {
             "match_winner": {
                "selections": {
                   "team a": {"odds": 1.9, "bookmaker": "BookmakerA"},
                   "team b": {"odds": 2.0, "bookmaker": "BookmakerB"},
                   ...
                }
             }, ...
          }
        }
        
        Args:
            sport_key: Sport key (e.g., 'soccer_epl', 'basketball_nba')
            region: Region filter (e.g., 'us', 'uk', 'eu')
            mkt: Market type (e.g., 'h2h', 'totals')
        """
        combined = {}
        for client in self.clients:
            try:
                source_events = client.fetch_odds(sport=sport_key, region=region, mkt=mkt)
            except Exception as e:
                print(f"[DEBUG] Error fetching from {client.name}: {e}")
                continue
            for e in source_events:
                name = e.get("name")
                if not name:
                    continue
                if name not in combined:
                    combined[name] = {"name": name, "markets": {}}
                
                # Process markets dict with market types as keys
                markets_data = e.get("markets", {})
                for market_key, selections_dict in markets_data.items():
                    if market_key not in combined[name]["markets"]:
                        combined[name]["markets"][market_key] = {"selections": {}}
                    for sel_name, sel_data in selections_dict.items():
                        # sel_data is a list of offers from multiple bookmakers
                        for offer in sel_data:
                            if isinstance(offer, dict):
                                odds = offer.get("odds")
                                bookmaker = offer.get("bookmaker", client.name)
                            else:
                                odds = offer
                                bookmaker = client.name
                            if odds is None:
                                continue
                            existing = combined[name]["markets"][market_key]["selections"].get(sel_name)
                            offers = existing["offers"] if existing else []
                            offers.append({"odds": float(odds), "bookmaker": bookmaker})
                            combined[name]["markets"][market_key]["selections"][sel_name] = {"offers": offers}
        
        # Convert offers to best-odds summary
        events = []
        for name, data in combined.items():
            markets = {}
            for mk, mv in data["markets"].items():
                selections = {}
                for sname, sdata in mv["selections"].items():
                    # Choose best odds per selection
                    best = max(sdata["offers"], key=lambda x: x["odds"])
                    selections[sname] = {"best": best, "offers": sdata["offers"]}
                markets[mk] = {"selections": selections}
            events.append({"name": name, "markets": markets})
        
        return events