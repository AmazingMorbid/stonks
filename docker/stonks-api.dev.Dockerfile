FROM python:3.8

WORKDIR /app/stonks-api
COPY ./stonks-api/Pipfile ./stonks-api/Pipfile.lock ./

WORKDIR /app/stonks-types
COPY ./stonks-types/ ./

WORKDIR /app/stonks-api
RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --dev

COPY ./stonks-api ./

ENV ENV=development

RUN chmod +x ./scripts/prestart.sh ./scripts/start.dev.sh

EXPOSE 8000

CMD ["./scripts/start.sh"]
