# Using GitHub CoPilot to Build and Odds Arbitrage App in Python

## Goal:

I wanted to see if I could build a full flask app by writing minimal code and having AI do the lion's share of the work.

## 1. Prompting and Troubleshooting the Initial Code

I started by trying to build a full application using python and nodeJS, but I don't really know node that well, so finally asked it to build me an arbitrage app fully in python. It was useful in putting together the entire project and starting with some base code, including ways to call the bookmakers once I get their API keys and setting up an environment variable. However, when I first tried to run the flask code, it gave me a circular call error, so then I prompted it to move the functions that are circular into a separate "helpers.py" file.

Once we solved this problem, the app started. Let's see what we got:

[First App Iteration](first_look.png)

Not bad, a little plain, but I can see what we're working with. Now to get the odds together and dig deeper into the code to see what we're dealing with.

## 2. Gathering bookmaker odds

I googled bookmaker odds API and clicked the first link. It was free I guess. The odds API (https://the-odds-api.com/).

Had to create a notebook to test the api call and find out how to get the odds that I needed, then incorporate that into the code (all using copilot of course). This was pretty easy once I got the key working and figured out the endpoints overall. Now it's running.

## 3. Retooling the code

I think asked copilot to incorporate the code from api_test.ipynb into the main code. When I ran it, no odds showed up, but I could see that they were being aggregated using a print statement.

I asked copilot to fix this and it got the odds to show, but with a few errors:

[First Look at Odds](odds_showing_initial.png)

You can see that it doesn't show the other team or any other books even though they exist. It seems to only grab the best. It's also not showing me arbitrage, just what appears to be the best odds for a game.

I prompted the AI some more and fed it the example JSON output so that it knew what to look for. This time it fixed the issue and now we can see which bookmaker has the best odds. I also switched to over unders instead of moneyline betting.

[Updated Output](fixed_with_bookies.png)

How cool! I also had it update the layout to be more visually appealing and well, it definitely is more visually appealing. Unfortunately, I'm not seeing any arbitrage. I also may want to look at other sports and have tabs for soccer, minor league baseball, etc. So let's add that in there! And where is the date / time of the game? That would be helpful!

Wow we added it!

[Added New Leagues](added_leagues.png)

Now we have a few different leagues and we'll have to format for what's in season. Or we can set it up to call /sports in the API and then just grab all the sports that are there, although it could be overkill. 

At the moment though, I'm happy with this. Even though in the screenshot it shows penguins vs penguins instead. Another cool feature will be to switch between h2h, spreads, and totals. So I guess I'll ad that in next. 

Ok, we did that and added various betting opportunities across the leagues. Now we have big arbitrage opportunities. Look at that.

[Arbitrage Opportunities](arbitrage.png)

Finally, I asked it to read through the folder and find unused code that can be deleted. And it removed the ability to process the moneyline odds, so we have to go back and fix that. I told it to revert the change and it fixed it. Building an app in a couple hours (with credit limits) using GitHub co-pilot. Neat!