FROM python:3.8

WORKDIR /app/stonks-api
COPY ./stonks-api/Pipfile ./stonks-api/Pipfile.lock ./

WORKDIR /app/stonks-types
COPY ./stonks-types/ ./

WORKDIR /app/stonks-api
RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --dev && \
    pip uninstall pipenv -y

COPY ./stonks-api ./

ENV ENV=production

RUN chmod +x ./scripts/prestart.sh ./scripts/start.sh

EXPOSE 8000

ENTRYPOINT ./scripts/start.sh
