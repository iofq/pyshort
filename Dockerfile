FROM debian:stable

MAINTAINER iofq "mail@iofq.net"

RUN apt update -y && \
    apt install -y python-pip python-dev git

RUN git clone https://github.com/iofq/pyshort /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]
