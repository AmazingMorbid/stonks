FROM python:3.8-slim

WORKDIR /app

# Install cron
RUN apt-get -y update && \
    apt-get -y --no-install-recommends install cron

COPY Pipfile Pipfile.lock ./

COPY ./libs/ ./libs/

RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile --dev

COPY ./backend/ ./backend/

COPY ./scripts ./scripts/
RUN chmod +x ./scripts/*.sh

WORKDIR /app/backend

# Thanks to that, celery worker won't scream about root, duh
RUN useradd --shell /bin/bash celery

# Copy crontab file to the cron directory
COPY ./backend/stonks-scraper/crontab /etc/cron.d/scrap-cron

# 1. Give execution rights on the cron job
# 2. Create the log file to be able to run tail
# 3. Install Cron
RUN chmod 0644 /etc/cron.d/scrap-cron && \
    touch /var/log/cron.log

EXPOSE 80
