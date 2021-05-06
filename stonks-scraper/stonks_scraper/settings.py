import sentry_sdk

SPIDER_MODULES = ["stonks_scraper.spiders"]

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'

sentry_sdk.init(
    "https://b6b0ca9a148547e3a8f9380d1d2eb360@o577912.ingest.sentry.io/5747985",
    sample_rate=0.2,
)
