FROM python:3.8-slim

WORKDIR /app/device-recognizer-api
COPY ./device-recognizer-api/Pipfile ./device-recognizer-api/Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --deploy

COPY ./device-recognizer-api ./

ENV ENV=production

RUN chmod +x ./scripts/start.sh

EXPOSE 80

CMD ["./scripts/start.sh"]
