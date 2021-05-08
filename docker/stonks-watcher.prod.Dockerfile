FROM python:3.8-slim

WORKDIR /app
COPY ./stonks-watcher/Pipfile ./stonks-watcher/Pipfile.lock ./stonks-watcher/


COPY ./stonks-types ./stonks-types
COPY ./allegro-sdk ./allegro-sdk
COPY ./olx-sdk ./olx-sdk

RUN ls && ls stonks-watcher && ls allegro-sdk

WORKDIR /app/stonks-watcher
RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY ./stonks-watcher ./

# Thanks to that, celery worker won't scream about root, duh
RUN useradd --shell /bin/bash celery

RUN chmod +x ./scripts/start-worker.sh ./scripts/start-beat.sh
