FROM python:3.8-slim

WORKDIR /app
COPY ./stonks-scraper/Pipfile ./stonks-scraper/Pipfile.lock ./stonks-scraper/


COPY ./stonks-types ./stonks-types
COPY ./allegro-sdk ./allegro-sdk
COPY ./olx-sdk ./olx-sdk

WORKDIR /app/stonks-scraper
RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY ./stonks-scraper ./

# Copy crontab file to the cron directory
COPY ./stonks-scraper/crontab /etc/cron.d/scrap-cron

# 1. Give execution rights on the cron job
# 2. Create the log file to be able to run tail
# 3. Install Cron
RUN chmod 0644 /etc/cron.d/scrap-cron && \
    touch /var/log/cron.log && \
    apt-get -y update && \
    apt-get -y --no-install-recommends install cron && \
    chmod +x start.sh

# Run the command on container startup
CMD ["./start.sh"]
