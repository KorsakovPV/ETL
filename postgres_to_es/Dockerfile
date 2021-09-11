FROM python:3.9-slim-buster

RUN mkdir /etl
WORKDIR /etl

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install psycopg2 and curl
#RUN apt-get update && apt-get install postgresql-dev gcc python3-dev musl-dev

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /etl/
RUN pip install -r requirements.txt
COPY . .

CMD python -u etl.py
