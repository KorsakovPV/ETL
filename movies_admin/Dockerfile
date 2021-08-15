FROM python:3.7.4

WORKDIR /code

RUN mkdir -p requirements

COPY requirements/*.txt requirements/

RUN pip install -r requirements/production.txt

COPY . .

CMD gunicorn wsgi:application --bind 0.0.0.0:8000
