FROM python:3.9

WORKDIR /app/stonks-watcher
COPY ./stonks-watcher/Pipfile ./stonks-watcher/Pipfile.lock ./

WORKDIR /app
COPY ./stonks-types ./stonks-types
COPY ./allegro-sdk ./allegro-sdk
COPY ./olx-sdk ./olx-sdk

WORKDIR /app/stonks-watcher
RUN pip install pipenv && \
    pipenv install --dev --system && \
    pip uninstall pipenv -y

COPY ./stonks-watcher ./

ENV API_URL="http://stonks-api:8000" \
    OFFER_DOWNLOAD_INTERVAL=1 \
    OFFER_UPDATE_INTERVAL=1 \
    OFFER_UPDATE_OLDER_THAN=30

CMD ["python", "main.py"]
