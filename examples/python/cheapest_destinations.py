"""Where can I fly cheapest? Google Flights Explore from one origin, cheapest first.

Example: week-long round trips from London to anywhere in Europe; Google picks each
destination's cheapest dates in the coming months.

    pip install apify-client
    export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
    python cheapest_destinations.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "exploreFrom": ["London"],         # airport (LHR), city code (LON) or city name; several allowed
    "exploreTo": ["europe"],           # or ["anywhere"], ["asia", "oceania"], ...
    "flexibleDates": True,             # False: use departDate/returnDate or daysAhead instead
    "tripType": "round_trip",
    "region": "GB",                    # prices in GBP
    "maxStops": "nonstop",
    "maxDestinations": 25,
})

for d in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{d['rank']:>2}. {d['destination'][:22]:22} {d['country'][:16]:16} {d['price']:>6} {d['currency']}  "
          f"{d['departDate']} → {d['returnDate']}  {d['airline']}")
