FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/
