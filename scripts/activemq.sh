#!/usr/bin/env bash
set -eu

ROOT="`dirname $0`/.."
ROOT=`readlink -m $ROOT`

wget http://apache.rediris.es/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.tar.gz
tar -xvzf apache-activemq-5.8.0-bin.tar.gz
sudo mv apache-activemq-5.8.0 /opt
sudo ln -sf /opt/apache-activemq-5.8.0/ /opt/activemq
sudo adduser -system activemq --shell /bin/bash
sudo ln -sf /opt/activemq/bin/activemq /etc/init.d/
sudo update-rc.d activemq defaults
sudo /etc/init.d/activemq setup /etc/default/activemq
sudo chown root:nogroup /etc/default/activemq
sudo chmod 600 /opt/apache-activemq-5.8.0/conf/jmx.access
sudo chmod 600 /opt/apache-activemq-5.8.0/conf/jmx.password
sudo cp ${ROOT}/extra_cookbooks/activemq_mco/templates/default/activemq.xml.erb \
    /opt/activemq/conf/activemq.xml
sudo cp ${ROOT}/extra_cookbooks/activemq_mco/templates/default/keystore.jks \
        /opt/activemq/conf/keystore.jks
sudo cp ${ROOT}/extra_cookbooks/activemq_mco/templates/default/truststore.jks \
        /opt/activemq/conf/truststore.jks
sudo /etc/init.d/activemq start
