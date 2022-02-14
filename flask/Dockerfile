FROM python:3.8

RUN apt-get update

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["uwsgi","app.ini"]