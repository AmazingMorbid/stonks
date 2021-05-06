import sentry_sdk

from sentry_sdk.integrations.celery import CeleryIntegration
from celery import Celery

from config import config

app = Celery("stonks_watcher")
app.config_from_object("celeryconfig")
app.conf.beat_schedule = {
    "Periodic-prices-update": {
        "task": "prices.tasks.periodic_prices_update",
        "schedule": config["prices"]["update_interval"] * 60,
        "args": ()
    },
    "Periodic-offers-update": {
        "task": "offers.tasks.periodic_offers_update",
        "schedule": config["offers"]["update_interval"] * 60,
        "args": ()
    },
}

sentry_sdk.init(
    dsn='https://f1e132df10f04ba398e0750959149471@o577912.ingest.sentry.io/5733971',
    integrations=[CeleryIntegration()],
    sample_rate=0.2,
)
