import os

import sentry_sdk

SPIDER_MODULES = ["stonks_scraper.spiders"]

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'

SENTRY_DSN = os.getenv("SENTRY_DSN", None)
if SENTRY_DSN is not None:
    sentry_sdk.init(
        SENTRY_DSN,
        sample_rate=0.2,
        environment=os.getenv("ENV", "development")
    )

# LOG_FILE = "logs.log"
# LOG_ENABLED = True
