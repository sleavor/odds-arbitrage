from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from aggregator.odds_aggregator import OddsAggregator
from aggregator.arbitrage import find_arbitrage_opportunities

load_dotenv()  # loads .env if present

app = Flask(__name__, template_folder="templates", static_folder="static")

# create aggregator which will only enable clients with configured API keys
aggregator = OddsAggregator()

# Supported sports with their API keys
SPORTS = {
    "soccer_epl": {"name": "EPL Soccer", "sport_key": "soccer_epl", "region": "us"},
    "basketball_nba": {"name": "NBA", "sport_key": "basketball_nba", "region": "us"},
    "baseball_mlb": {"name": "MLB", "sport_key": "baseball_mlb", "region": "us"},
    "ice_hockey_nhl": {"name": "NHL", "sport_key": "icehockey_nhl", "region": "us"},
}

# Supported markets
MARKETS = {
    "h2h": {"name": "Moneyline", "description": "Match Winner"},
    "spreads": {"name": "Spread", "description": "Point Spread"},
    "totals": {"name": "Over/Under", "description": "Total Points"},
}

@app.route("/")
def index():
    sport = request.args.get("sport", "baseball_mlb")
    market = request.args.get("market", "h2h")
    
    # Get sport config or default to first
    sport_config = SPORTS.get(sport, list(SPORTS.values())[0])
    
    # Get market from MARKETS (default to h2h if invalid)
    market_config = MARKETS.get(market, MARKETS["h2h"])
    mkt = market_config.get("key", market)
    
    # Fetch events for the selected sport and market
    events = aggregator.aggregate(sport_key=sport_config["sport_key"], region=sport_config["region"], mkt=mkt)
    opportunities = find_arbitrage_opportunities(events)
    
    return render_template("index.html", events=events, opportunities=opportunities, sports=SPORTS, markets=MARKETS, current_sport=sport, current_market=market)

if __name__ == "__main__":
    app.run(debug=True)