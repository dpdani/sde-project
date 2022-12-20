FROM python:3.11-alpine3.17

RUN apk add bash

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY kappa/pyproject.toml .
RUN pip install -r pyproject.toml

COPY . .

CMD "cd kappa && kappa"
