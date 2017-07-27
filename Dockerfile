FROM peragro/peragro-at
MAINTAINER Peragro-Team

# Installing Elasticsearch Dependencies
RUN apt-get update && apt-get install -y default-jre
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections &&   apt-get update &&   apt-get install -y software-properties-common &&  add-apt-repository -y ppa:webupd8team/java &&   apt-get update &&   apt-get install -y oracle-java8-installer  &&   rm -rf /var/lib/apt/lists/* &&   rm -rf /var/cache/oracle-jdk8-installer

# Downloading and Installing Elasticsearch
RUN wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.1/elasticsearch-2.3.1.deb && dpkg -i elasticsearch-2.3.1.deb

# To make sure Elasticsearch starts and stops automatically with the server, add its init script to the default runlevels.
RUN systemctl enable elasticsearch.service

# download and setup peragro-index
ARG CACHEBUST=1
ADD . /opt/peragro-index
RUN /opt/peragro-index && python3 setup.py develop
