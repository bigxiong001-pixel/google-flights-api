// Google Flights fares from Node.js: every flight on a route and date.
//
//   npm install apify-client
//   APIFY_TOKEN=... node quickstart.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('xpandalabs/google-flights-fare-monitor').call({
    routes: ['LHR-JFK'],
    daysAhead: 21,
    region: 'GB',          // GBP prices
    sortBy: 'price',
    maxFlightsPerSearch: 10,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const f of items) {
    console.log(`${f.departureTime}-${f.arrivalTime} ${f.flightNumbers.join('/').padEnd(16)} ${f.airline.slice(0, 24).padEnd(24)} stops ${f.stops}  ${f.price} ${f.currency}`);
}
