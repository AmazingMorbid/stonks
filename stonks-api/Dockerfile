FROM python:3.9

WORKDIR /app/stonks-api
COPY ./stonks-api/Pipfile stonks-api/Pipfile.lock ./

WORKDIR /app/stonks-types
COPY ./stonks-types/ ./

WORKDIR /app/stonks-api
RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --dev && \
    pip uninstall pipenv -y

COPY ./stonks-api ./

EXPOSE 8000

WORKDIR /app/stonks-api
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000 --reload
