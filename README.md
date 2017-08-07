peragro-index
==========

Elastic search based index for Peragro metadata

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

    $ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.deb
    $ sudo dpkg -i elasticsearch-5.5.1.deb

To make sure Elasticsearch starts and stops automatically, add its init script to the default runlevels with the command:

    $ sudo update-rc.d elasticsearch defaults
    
start Elasticsearch

    $ sudo service elasticsearch start

#### Install peragro-index
**Clone Peragro-index:**

    $ git clone https://github.com/peragro/peragro-index.git

**Install Peragro-index:**

    $ cd peragro-index
    $ sudo python3 setup.py develop

