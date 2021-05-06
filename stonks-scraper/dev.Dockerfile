FROM python:3.9

WORKDIR /app/stonks-scraper
COPY ./stonks-scraper/Pipfile ./stonks-scraper/Pipfile.lock ./

WORKDIR /app
COPY ./stonks-types ./stonks-types
COPY ./allegro-sdk ./allegro-sdk
COPY ./olx-sdk ./olx-sdk


WORKDIR /app/stonks-scraper
RUN pip install pipenv && \
    pipenv install --dev --system && \
    pip uninstall pipenv -y

COPY ./stonks-scraper ./

ENTRYPOINT scrapy crawl olx_spider
