peragro-index
==========

Elastic search based index for Peragro metadata

## Installation with Docker (Recommended)

**Install Docker**

Follow the [instructions](https://docs.docker.com/engine/installation/) to install docker for your system

**Now Pull the Docker image from docker hub**

    $ docker pull peragro/peragro-index

#### Run peragro-index through docker using local files
**Now run the container in background**

    $ docker run -d -v /local/path/:/peragro --name index -p 9200:9200 peragro/peragro-index

Note: This will automatically starts elasticsearch and opens port 9200 from the container to the host.
Open http://localhost:9200 on your browser to check if its running.

**Execute the following command to index**

    $ docker exec -ti index pt a /peragro/file.blend -f json-pretty | pt index elastic
    
## Installation (locally)
#### Installing dependencies:

**Install elasticsearch**

First, you need to install OpenJDK

    $ sudo apt-get update
    $ sudo apt-get install default-jre

To verify your JRE is installed and can be used, run the command:

    $ java -version

Installing Java 8

    $ sudo add-apt-repository -y ppa:webupd8team/java
    $ sudo apt-get update

Install the latest stable version of Oracle Java 8 with this command (and accept the license agreement that pops up):

    $ sudo apt-get install oracle-java8-installer

**Downloading and Installing Elasticsearch**

    $ wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    $ sudo apt-get update && sudo apt-get install apt-transport-https
    $ echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list
    $ sudo apt-get update && sudo apt-get install elasticsearch

For more detailed info on installation, see [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)
    
start Elasticsearch

    $ sudo service elasticsearch start

#### Install peragro-index

**Clone Peragro-index:**

    $ git clone https://github.com/peragro/peragro-index.git

**Install Peragro-index:**

    $ cd peragro-index
    $ sudo python3 setup.py develop

**Indexing**

    $ pt a ../perargo-test-files/mesh/blender/cube1.blend -f json-pretty | pt index elastic
