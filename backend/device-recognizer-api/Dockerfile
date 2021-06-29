FROM python:3.8

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY . .

EXPOSE 8010

CMD ["pipenv", "run", "start"]
