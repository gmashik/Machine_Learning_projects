FROM python:3.9.6-slim

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload