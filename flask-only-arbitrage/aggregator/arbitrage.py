from typing import List, Dict
import math

def find_arbitrage_opportunities(events: List[Dict]) -> List[Dict]:
    opportunities = []
    for ev in events:
        for market_name, market in ev["markets"].items():
            selections = market["selections"]
            # collect best odds for each outcome
            odds_list = []
            for sname, sdata in selections.items():
                odds = sdata["best"]["odds"]
                bookmaker = sdata["best"]["bookmaker"]
                odds_list.append({"selection": sname, "odds": odds, "bookmaker": bookmaker})
            if len(odds_list) < 2:
                continue
            # check arbitrage by sum of reciprocals
            s_inv = sum(1.0 / o["odds"] for o in odds_list)
            if s_inv < 1.0 - 1e-12:
                # compute stakes for a total outlay (e.g., 100)
                total = 100.0
                stakes = []
                for o in odds_list:
                    stake = (total * (1.0 / o["odds"])) / s_inv
                    stakes.append({"selection": o["selection"], "bookmaker": o["bookmaker"], "odds": o["odds"], "stake": round(stake, 2)})
                payout = round(stakes[0]["stake"] * odds_list[0]["odds"], 2)  # same for all if computed correctly
                profit = round(payout - total, 2)
                opportunities.append({
                    "event": ev["name"],
                    "market": market_name,
                    "odds": odds_list,
                    "stakes": stakes,
                    "total_stake": total,
                    "payout": payout,
                    "profit": profit,
                    "arbitrage_percent": round((1.0 - s_inv) * 100, 4)
                })
    # sort by profit descending
    opportunities.sort(key=lambda x: x["profit"], reverse=True)
    return opportunities