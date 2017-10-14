FROM python:3.6.2-alpine3.6 as builder

RUN apk — update upgrade \
  && apk add --update \
              gcc \
              musl-dev \
              postgresql-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

FROM python:3.6.2-alpine3.6

RUN apk add --no-cache libpq

COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

COPY . /app

WORKDIR /app

# RUN python manage.py collectstatic --noinput

# CMD gunicorn -w 1 nba_stats.wsgi:application -b 0.0.0.0:8000
CMD python manage.py runserver 0.0.0.0:8000