# Track prices for locally sold Apple products

This application scrapes Apple listings from:
- Okidoki
- Soov
- Hinnavaatlus

Scraper is supposed to run daily and all price changes are recorded in the database. Currently not updating the data very often to keep OpenAI spending low.

Pet project to help people flipping Apple products (I also had a suitable domain name laying around, with no use).

## Features

- Product scraper for 3 different marketplaces
- Product classifier with OpenAI to better understand each product and it's features
- Web interface created with NextJS
- Price history graph for each listing
- Add listings to favorites
- Apple MacOS themed website design
