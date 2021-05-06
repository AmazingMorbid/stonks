FROM python:3.9

WORKDIR /app

COPY ./stonks-scraperPipfile Pipfile.lock ./
COPY libs/ ./libs

CMD ["ls"]

RUN pip install pipenv && \
    pipenv install --dev --system && \
    pip uninstall pipenv -y


CMD ["scrapy", "crawl", "olx_spider"]
