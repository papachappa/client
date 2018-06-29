FROM ubuntu:16.04

LABEL maintainer="ailin@luxoft.com"

COPY Docker/* . /app/
WORKDIR /app/

ENV DOCKER=true

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
                        curl \
                        apt-transport-https \
                        python3.5 \
                        python3-setuptools \
                        python3-pip \
                        python3-dev \
                        libcurl4-openssl-dev \
                        gcc \
                        libffi-dev \
                        libssl-dev \
                        iputils-ping \
                        sispmctl \
                        openssh-client \
                        usbutils \
                        pciutils \
                        iproute2 \
    && ./add_external.sh \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
                        loewe-bizlogic \
                        loewe-bizmon \
                        loewe-webiz \
                        lstreamer=0-dev \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm ./add_external.sh \
    && mkdir /var/client/

RUN pip3 install -r requirements.txt
