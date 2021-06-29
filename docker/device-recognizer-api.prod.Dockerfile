FROM python:3.8-slim

WORKDIR /app/device-recognizer-api
COPY ./backend/device-recognizer-api/Pipfile ./backend/device-recognizer-api/Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --deploy

COPY ./backend/device-recognizer-api ./

ENV ENV=production

EXPOSE 8010

CMD ["pipenv", "run", "start"]
