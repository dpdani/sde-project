FROM python:3.11-alpine3.17

RUN apk add bash

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY pyproject.toml .
COPY . .
RUN pip install -e .

CMD "kappa"
