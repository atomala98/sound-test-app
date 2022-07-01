FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY soundtestapp/requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app
