FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /code/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
