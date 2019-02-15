FROM ubuntu:latest

RUN apt-get update && apt-get install -q=2 wget python3 python3-pip firefox

RUN pip3 install selenium dateparser

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz && tar xf geckodriver-v0.23.0-linux64.tar.gz && mv geckodriver /usr/local/bin && rm geckodriver-v0.23.0-linux64.tar.gz

ADD paper-archive.py .
ADD schema.sql .

CMD ["python3", "-u", "paper-archive.py"]
