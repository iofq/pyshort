FROM debian:stable

MAINTAINER iofq "mail@iofq.net"

RUN apt update -y && \
    apt install -y python3-pip python-dev git python3

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]
