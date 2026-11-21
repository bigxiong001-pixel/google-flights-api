# Google Flights API (no API key): flight prices, fare calendar and price alerts

Google shut down its flight search API (QPX Express) in 2018 and has no public API for Google Flights results. This repo shows how to get Google Flights data as JSON anyway, through the **[Google Flights Scraper & Fare Monitor](https://apify.com/xpandalabs/google-flights-fare-monitor)** on Apify. You call it like an API from Python, JavaScript, cURL, n8n, Make or Zapier: **no Google API key, no airline or GDS account**.

## What you get

- **Every flight** on a route and date: airline, flight numbers, departure and arrival times, duration, stops, layovers, aircraft, legroom, CO₂ and the total price for your passengers.
- **Fare calendar**: the cheapest fare for each departure date, Google's verdict (**low / typical / high**), the typical price range and the 60-day price history. Find the cheapest day to fly.
- **Price alerts**: price drops and rises since the previous run, and fares at or below your target price. With `onlyChanges` you only get, and only pay for, fares that moved.
- One-way and round trips, adults and children, economy to first class, stop and airline filters, 15 currency presets.
- Routes as airport codes (`JFK-LAX`), city codes for every airport in a city (`NYC-LON`), city names (`New York to London`) or a Google Flights link.

## Quick start

1. Create a free [Apify account](https://console.apify.com/sign-up) and copy your API token from **Settings → Integrations**. The free plan includes $5 of monthly credit, about 5,000 flights.
2. `pip install apify-client` and `export APIFY_TOKEN=...`
3. Run an example:

| Example | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Nonstop flights JFK → LAX, cheapest first |
| [`examples/python/fare_calendar.py`](examples/python/fare_calendar.py) | Cheapest day to fly London → New York in the next 30 days |
| [`examples/python/price_drop_alert.py`](examples/python/price_drop_alert.py) | Daily fare alert with a target price |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Node.js: London → New York in GBP |
| [`examples/curl/run-sync.sh`](examples/curl/run-sync.sh) | One HTTP request in, JSON rows out |

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "routes": ["JFK-LAX"],
    "departDate": "2026-12-20",
    "maxStops": "nonstop",
    "sortBy": "price",
})
for f in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f["airline"], f["flightNumbers"], f["departureTime"], f["price"], f["currency"])
```

## Output

Real rows from the Actor: [`sample-output/flight-row.json`](sample-output/flight-row.json) (one flight) and [`sample-output/fare-calendar-row.json`](sample-output/fare-calendar-row.json) (one route and date).

| Field | Meaning |
|---|---|
| `airline`, `flightNumbers`, `departureTime`, `arrivalTime`, `durationMinutes`, `stops`, `layovers`, `aircraft`, `co2Kg` | The flight |
| `price`, `pricePerPassenger`, `currency` | Total for all passengers (round trips: the whole trip) |
| `flightPriceLevel`, `typicalPriceLow`, `typicalPriceHigh` | Where the price falls in Google's typical range |
| `cheapestPrice`, `priceLevel`, `priceHistory` | Fare calendar rows (`"outputMode": "cheapest"`) |
| `changeType`, `previousPrice`, `priceChangePct`, `lowestPriceSeen`, `belowTargetPrice` | Changes since the previous run and target-price alert |
| `segments[]`, `googleFlightsUrl` | Each leg in detail, and the search on Google Flights |

## Main inputs

| Input | Example |
|---|---|
| `routes` | `["JFK-LAX", "NYC-LON", "上海到东京"]` |
| `departDate` / `daysAhead` | `"2026-12-20"` / `14` (rolling date for schedules) |
| `tripType`, `returnDate`, `tripLengthDays` | `"round_trip"`, `"2026-12-27"`, `7` |
| `datesToCheck`, `dateStepDays` | `30`, `1` (many departure dates in one run) |
| `adults`, `children`, `cabin` | `2`, `1`, `"business"` |
| `maxStops`, `airlines` | `"nonstop"`, `["DL", "United"]` |
| `outputMode` | `"flights"` (every flight) or `"cheapest"` (fare calendar) |
| `region` or `currency` | `"GB"`, `"JP"`, `"HK"`, ... or `"EUR"` |
| `targetPrice`, `onlyChanges` | `700`, `true` |

Full reference: [input schema](https://apify.com/xpandalabs/google-flights-fare-monitor/input-schema).

## Pricing

Pay per result, no start fee: **$1 per 1,000 flights**, or **$2 per 1,000 fare-calendar rows**. Paid Apify plans get up to 30% off. Set a maximum cost per run and the Actor stops at that limit. Details on the [pricing page](https://apify.com/xpandalabs/google-flights-fare-monitor/pricing).

## AI agents and MCP

AI assistants (Claude, ChatGPT, Cursor and others) can call the Actor as a tool through the [Apify MCP server](https://mcp.apify.com), for example to answer "cheapest nonstop from London to New York next Friday" with live fares.

## Ready-made examples on Apify

- [Cheapest day to fly New York to London](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/cheapest-day-to-fly-new-york-london)
- [Flight price drop alert: London to New York](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/flight-price-drop-alert)
- [Nonstop flights JFK to LAX, cheapest first](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/nonstop-flights-jfk-lax)
- [Family round-trip fares Hong Kong to Bangkok](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/family-round-trip-hong-kong-bangkok)
- [Business class fares Singapore to London](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/business-class-singapore-london)
- [Shanghai to Tokyo flight prices in CNY](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/shanghai-tokyo-flight-prices-cny)

## Related

- [Google Hotels API](https://github.com/bigxiong001-pixel/google-hotels-api): hotel prices, every booking site's rate, rate parity
- [Google Trends API](https://github.com/bigxiong001-pixel/google-trends-api): rising and falling keywords, breakout searches, trending now

## Questions

Open an issue on the [Actor's Issues tab](https://apify.com/xpandalabs/google-flights-fare-monitor/issues) or in this repo.

The data is the public Google Flights results page any visitor sees. You are responsible for using it in line with applicable laws and Google's terms. The code in this repo is MIT-licensed.
