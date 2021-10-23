FROM rofrano/vagrant-provider:ubuntu

RUN apt-get update && apt-get install -y \
    locales \
    curl \
    wget \
    lsb-release \
    python \
    ca-certificates \
    gnupg2 \
    software-properties-common \
    apt-utils \
    iputils-ping \
    net-tools \
    nano \
    less
