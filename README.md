# Arbitrage Bot

I created this vibecoding with GitHub Co-Pilot to test how easy building an app was. It was easier than I expected it to be. That entire app is under `flask-only-arbitrage`. The most manual thing that I had to do was find and get odds with the-odds-api.

## Getting the API

I used [The Odds Api](https://the-odds-api.com) to get odds from multiple bookmakers. Feel free to use the API of your choice, but this one was free and easy to set up. Fair warning, you only get 500 calls per month and each time you switch between tabs in the app, it will run a new pull since it's not caching the data, which means those 500 can go quick. 

## Running the code

The app is ran by flask, so you'll need the right files. `requirements.txt` is in the flask-only-arbitrage app. That's where everything you would need is anyways. 

Set up your venv in flask-only-arbitrage and then run: `pip install -r requirements.txt`.

To run the app, all you have to do is activate the virtual environment and run `python app.py`. The command line will give you the link to the website, but it normally defaults to 127.0.0.1:5000.