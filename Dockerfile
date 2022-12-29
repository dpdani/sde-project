FROM python:3.11-alpine3.17

WORKDIR /app

COPY . .
RUN pip install -e .

CMD "kappa"
