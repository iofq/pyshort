#!/bin/bash

docker build -t pyshort .
docker rm -f pyshort

docker run -d \
	--name pyshort \
	-p 5000:5000 \
	--restart=unless-stopped \
	pyshort
