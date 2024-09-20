FROM python:3.11.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash

WORKDIR /home_housing_backend
COPY requirements.txt /home_housing_backend/
RUN pip install -r requirements.txt
COPY . /home_housing_backend/