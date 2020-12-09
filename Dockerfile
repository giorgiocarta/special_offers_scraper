FROM balenalib/raspberry-pi-debian:latest

LABEL maintainer="Giorgio Carta <giorgiocarta@gmail.com>"

RUN apt-get upgrade -y
RUN apt-get update -y


RUN apt-get install python3 -y
RUN apt-get install python3-dev -y
RUN apt-get install python3-pip -y
RUN apt-get install libxslt1-dev -y

RUN pip3 install --no-cache-dir setuptools

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./ /app
WORKDIR /app/shopping

#RUN pip3 install -e .

ENV PYTHONPATH=/app/shopping

CMD ["scrapy", "crawl", "lidl"]
