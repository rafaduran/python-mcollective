#!/usr/bin/env bash
set -eu

ROOT="`dirname $0`/.."
ROOT=`readlink -m $ROOT`

sudo apt-get install activemq -y

sudo cp ${ROOT}/extra_cookbooks/activemq_mco/templates/default/activemq.xml.erb \
    /etc/activemq/instances-available/main/activemq.xml
sudo ln -s /etc/activemq/instances-available/main/ /etc/activemq/instances-enabled/main
sudo /etc/init.d/activemq stop
sudo /etc/init.d/activemq start
