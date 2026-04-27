import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# The Odds API (single endpoint for multiple bookmakers)
ODDS_API_URL = os.getenv("ODDS_API_URL", "https://api.the-odds-api.com/v3")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")