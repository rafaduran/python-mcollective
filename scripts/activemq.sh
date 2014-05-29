#!/usr/bin/env bash
set -eu

ROOT=$(dirname $0)
ROOT=$(readlink -m $ROOT)

if [[ ! -f apache-activemq-5.9.1-bin.tar.gz ]]; then
    wget https://repository.apache.org/content/repositories/releases/org/apache/activemq/apache-activemq/5.9.1/apache-activemq-5.9.1-bin.tar.gz
fi

if [[ ! -d /opt/apache-activemq-5.9.1 ]]; then
    tar -xvzf apache-activemq-5.9.1-bin.tar.gz
    sudo mv apache-activemq-5.9.1 /opt
fi

if [[ ! -L /opt/activemq ]]; then
    sudo ln -sf /opt/apache-activemq-5.9.1/ /opt/activemq
fi

sudo adduser -system activemq --shell /bin/bash
sudo ln -sf /opt/activemq/bin/activemq /etc/init.d/
sudo update-rc.d activemq defaults
sudo /etc/init.d/activemq setup /etc/default/activemq
sudo chown root:nogroup /etc/default/activemq
sudo chmod 600 /opt/apache-activemq-5.9.1/conf/jmx.access
sudo chmod 600 /opt/apache-activemq-5.9.1/conf/jmx.password
sudo cp ${ROOT}/activemq.xml /opt/activemq/conf/activemq.xml
sudo cp ${ROOT}/keystore.jks /opt/activemq/conf/keystore.jks
sudo cp ${ROOT}/truststore.jks /opt/activemq/conf/truststore.jks
sudo /etc/init.d/activemq start
