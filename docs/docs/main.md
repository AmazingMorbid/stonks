---
sidebar_position: 1
---

# stonks

Unfortunately, because I'm a noob, this project is split into two parts:
- stonks-watcher - takes care of updating old offers and finding profit.
- stonks-scraper - downloads offers for the first time.  

## Why
OLX requires verification for API apps. I overcome this by using their other API
which works without registering an app. The problem is, I have no idea how to
filter and sort offers from that API, so I'm using scrapy to scrap new offers from their website..., 
and I don't know how to use scrapy with the rest of my app, so I just split these into two separate containers,
that share the same database via API.
**Don't even ask me what I'll do when they disable this API**
