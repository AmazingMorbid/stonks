FROM python:3.9

WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --ignore-pipfile --dev && \
    pip uninstall pipenv -y

COPY . .

EXPOSE 8000

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000 --reload
