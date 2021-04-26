---
sidebar_position: 2
---

# Configuration

**stonks-watcher** can be configured using environmental variables.

## Environmental variables

`API_URL` (required)

This is the URL that will be used to communicate with an API.

`ALLEGRO_CLIENT_ID` (required)

Client ID of registered allegro api app.

`ALLEGRO_CLIENT_SECRET` (required)

Client secret of registered allegro api app.

`OFFER_UPDATE_INTERVAL` (Default: ```1```)  

How often **in minutes** stonks-watcher should ask API for outdated offers and update them. 
Note that "outdated" does not mean an offer has expired, but the database copy of that offer did.
Updating means re-downloading this offer from the internet and updating the stonks database.  
When an offer is updated, stonks-watcher will automatically look for possible stonkses.

`OFFER_UPDATE_OLDER_THAN` (Default: ```30```)

When stonks-watcher triggers offers update, it will ask the API for offers that are older than 30 minutes

`SENTRY_DSN` (optional)

You can use [Sentry](https://sentry.io) to log production errors. In Sentry, create project for **celery**
and set `SENTRY_DSN` to your project's DSN.
