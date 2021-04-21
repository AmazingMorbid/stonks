---
sidebar_position: 2
---

# Configuration

**stonks-watcher** can be configured using environmental variables.

## Environmental variables

`API_URL`

This is the URL that will be used to communicate with an API.

`OFFER_UPDATE_INTERVAL` (Default: ```1```)  

How often **in minutes** stonks-watcher should ask API for outdated offers and update them. 
Note that "outdated" does not mean an offer has expired, but the database copy of that offer did.
Updating means re-downloading this offer from the internet and updating the stonks database.  
When an offer is updated, stonks-watcher will automatically look for possible stonkses.

`OFFER_UPDATE_OLDER_THAN` (Default: ```30```)

When stonks-watcher triggers offers update, it will ask the API for offers that are older than 30 minutes