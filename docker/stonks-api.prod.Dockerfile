FROM python:3.8-slim

WORKDIR /app
COPY Pipfile Pipfile.lock ./

COPY ./libs ./libs

RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY ./backend/ ./backend

WORKDIR /app/backend

# Thanks to that, celery worker won't scream about root, duh
RUN useradd --shell /bin/bash celery

RUN chmod +x ./scripts/start-worker.sh ./scripts/start-beat.sh

EXPOSE 80

