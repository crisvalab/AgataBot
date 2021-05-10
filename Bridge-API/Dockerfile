FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN sudo apt-get install -y sqlite3 libsqlite3-dev
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/agatacloud.db

RUN pip install -r requirements.txt

CMD ["python", "apiservice.py"]