FROM python:3.8-slim

WORKDIR /app
COPY ./stonks-watcher/Pipfile ./stonks-watcher/Pipfile.lock ./stonks-watcher/


COPY ./stonks-types ./stonks-types
COPY ./allegro-sdk ./allegro-sdk
COPY ./olx-sdk ./olx-sdk

WORKDIR /app/stonks-watcher
RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY ./stonks-watcher ./

RUN chmod +x ./scripts/start-worker.sh ./scripts/start-beat.sh
