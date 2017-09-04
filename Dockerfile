FROM peragro/peragro-at
MAINTAINER Peragro-Team

# Installing Elasticsearch Dependencies
RUN apt-get update && apt-get install -y default-jre
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections &&   apt-get update &&   apt-get install -y software-properties-common &&  add-apt-repository -y ppa:webupd8team/java &&   apt-get update &&   apt-get install -y oracle-java8-installer  &&   rm -rf /var/lib/apt/lists/* &&   rm -rf /var/cache/oracle-jdk8-installer

# Downloading and Installing Elasticsearch
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
    && apt-get update && apt-get install apt-transport-https \
    && echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-5.x.list \
    && apt-get update && apt-get install --no-install-recommends elasticsearch

ENV PATH=$PATH:/usr/share/elasticsearch/bin

WORKDIR /usr/share/elasticsearch

RUN set -ex \
	&& for path in \
		./data \
		./logs \
		./config \
		./config/scripts \
	; do \
		mkdir -p "$path"; \
		chown -R elasticsearch:elasticsearch "$path"; \
done

COPY config ./config

# download and setup peragro-index
ARG CACHEBUST=1
ADD . /opt/peragro-index
RUN cd /opt/peragro-index && python3 setup.py develop

USER elasticsearch
CMD ["elasticsearch"]

EXPOSE 9200 9300
