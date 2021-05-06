FROM python:3.9

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --system && \
    pip uninstall pipenv -y

COPY . .

# Copy crontab file to the cron directory
COPY crontab /etc/cron.d/scrap-cron

# 1. Give execution rights on the cron job
# 2. Create the log file to be able to run tail
# 3. Install Cron
RUN chmod 0644 /etc/cron.d/scrap-cron && \
    touch /var/log/cron.log && \
    apt-get -y update && \
    apt-get -y --no-install-recommends install cron && \
    chmod +x start.sh

# Run the command on container startup
CMD ./start.sh
