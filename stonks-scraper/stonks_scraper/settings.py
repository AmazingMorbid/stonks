import sentry_sdk

SPIDER_MODULES = ["stonks_scraper.spiders"]

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'

sentry_sdk.init("http://a0ca55b95a3e4ce5be1ee8fbec4c1fb9@localhost:9000/2")
