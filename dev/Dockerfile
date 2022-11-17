FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN pip install -r /app/requirements.txt

CMD sleep 60 ; python manage.py migrate ; sleep 120 ; python manage.py sync_cassandra --database=stores_data ; python manage.py runserver 0.0.0.0:8000