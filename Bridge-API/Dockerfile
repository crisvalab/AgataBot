FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN apt update && apt upgrade -y
RUN apt-get install sqlite3 libsqlite3-dev -y
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/agatacloud.db

RUN pip install -r requirements.txt

CMD ["python", "apiservice.py"]