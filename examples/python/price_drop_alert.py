"""Flight price drop alert: run daily (cron, GitHub Actions or an Apify schedule).
Prints only fares that moved since the previous run or are at/below your target price.

    pip install apify-client
    export APIFY_TOKEN=...
    python price_drop_alert.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "routes": ["SFO-NRT", "LAX-HND"],
    "outputMode": "cheapest",     # cheapest fare per route and date
    "daysAhead": 45,              # rolls forward with the calendar
    "datesToCheck": 7,
    "targetPrice": 700,           # USD, total for all passengers
    "onlyChanges": True,          # first run = baseline; later runs return (and charge) only changes
})

for r in client.dataset(run["defaultDatasetId"]).iterate_items():
    flag = "TARGET HIT " if r.get("belowTargetPrice") else ""
    change = f"{r['changeType']} {r.get('priceChangePct') or ''}%" if r.get("previousPrice") else r["changeType"]
    print(f"{flag}{r['route']} {r['departDate']}: {r['cheapestPrice']} {r['currency']} ({change}), "
          f"Google says {r.get('priceLevel')}, {r.get('cheapestAirline')}")
