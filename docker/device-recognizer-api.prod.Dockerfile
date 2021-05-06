FROM python:3.8

WORKDIR /app/device-recognizer-api
COPY ./device-recognizer-api/Pipfile ./device-recognizer-api/Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --deploy

COPY ./device-recognizer-api ./

ENV ENV=production

RUN chmod +x ./scripts/start.sh

EXPOSE 8010

CMD ["./scripts/start.sh"]
