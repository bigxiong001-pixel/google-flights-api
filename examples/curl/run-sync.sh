#!/usr/bin/env bash
# Google Flights over plain HTTP: one request in, JSON rows out.
# The run-sync endpoint waits for the run (up to 300 s) and returns the dataset items directly.
#
#   APIFY_TOKEN=... ./run-sync.sh
set -euo pipefail

curl -sS -X POST \
  "https://api.apify.com/v2/acts/xpandalabs~google-flights-fare-monitor/run-sync-get-dataset-items?format=json" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
        "routes": ["SIN-BKK"],
        "daysAhead": 14,
        "region": "SG",
        "maxStops": "nonstop",
        "sortBy": "price",
        "maxFlightsPerSearch": 10
      }'
# Each row has airline, flight numbers, times, duration, stops, aircraft, CO2 and the total price.
# Use format=csv or format=xlsx for spreadsheets.
