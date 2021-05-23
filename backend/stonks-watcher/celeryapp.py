import os

import sentry_sdk
from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration

from config import config

app = Celery("stonks_watcher")
app.config_from_object("config.celeryconfig")
app.conf.beat_schedule = {
    # "Periodic-prices-update": {
    #     "task": "prices.tasks.periodic_prices_update",
    #     "schedule": config["prices"]["update_interval"],
    #     "args": ()
    # },
    # "Periodic-offers-update": {
    #     "task": "offers.tasks.periodic_offers_update",
    #     "schedule": config["offers"]["update_interval"] * 60,
    #     "args": ()
    # },
    # "Periodic_get_device_info": {
    #     "task": "offers.tasks.periodic_get_device_info",
    #     "schedule": config["offers"]["update_device_info_interval"] * 60,
    #     "args": ()
    # },
    "Periodic_find_stonks": {
        "task": "stonks.tasks.periodic_stonks_finder",
        "schedule": config["stonks"]["interval"] * 60,
        "args": ()
    },

}

SENTRY_DSN = os.getenv("SENTRY_DSN", None)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[CeleryIntegration()],
        sample_rate=0.2,
        environment=os.getenv("ENV", "development")
    )

# harmonogram
# chowanie ciał
# wszystkie dziwne rzeczy są zlewane na yandere deva
