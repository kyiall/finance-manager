FROM python:3.13-slim

WORKDIR /backend
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY . .
