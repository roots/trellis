FROM rofrano/vagrant-provider:ubuntu

RUN apt-get update \
    && apt-get install -y iproute2
