# stonks

## Story
I started earning some extra money by repairing smartphones.
I tried to make an app, that will show me potential offers without spending many hours on looking for them myself.
I started by looking for price differences between OLX and Allegro for every used device, from smartphones to printers.
It does somewhat work, but most (if not every) stonkses are false positives.
Algorithm that looks for stonkses needs a ton of filters for example: iPhone 8 case is interpreted as iPhone 8, which means that a false stonks will be created with ton of money to earn.
Saddly, it requires too much work for me to finish it and Allegro turned off the most important API route for unapproved apps.
So, I open sourced it.

## Installation
1. Clone the repository.
2. Run `docker-compose -f docker-compose.dev.yml up`.

## How does it work
This project is built on top of few modules: SQL database, message queue, celery worker and crud for scheduling tasks, OLX web scraper for harvesting offers, app API for communication between modules and frontend, and device recognision API for detecting device name in offer title built with Spacy.
Every couple of mintues `stonks-scraper` crawls OLX and scrapes latest offers, they're saved to database via API.
Then, device recognision API is used to get the name of the device, which is also saved to the database. That way, I can easily search for prices of the device on Allegro. Because Allegro API is limited to only 6 searches per minute, prices are saved to the database and then these prices are used later instead of calling Allegro.
Finally, `stonks-watcher` requests an offer from db, checks if it's price is lower than on Allegro, and creates stonks appropriately.
