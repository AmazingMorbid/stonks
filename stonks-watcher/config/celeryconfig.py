import os


## Broker settings.
broker_url = os.getenv("BROKER_URI", "pyamqp://stonks-broker:5672//")

# List of modules to import when the Celery worker starts.
imports = (
    "prices.tasks",
    "offers.tasks",
    "stonks.tasks",
)

# Serialization
task_serializer = "pickle"
result_serializer = "pickle"
event_serializer = "json"
accept_content = ["application/json", "application/x-python-serialize"]
result_accept_content = ["application/json", "application/x-python-serialize"]
