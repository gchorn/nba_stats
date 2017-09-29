FROM python:3.6.2-alpine3.6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . /app

WORKDIR /app

RUN python manage.py migrate

CMD gunicorn -w 2 nba_stats.wsgi:application -b 0.0.0.0:8000
