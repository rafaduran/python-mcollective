#!/usr/bin/env bash
set -eu

ROOT="`dirname $0`/.."
ROOT=`readlink -m $ROOT`

sudo apt-get install activemq -y

cp ${ROOT}/extra_cookbooks/activemq_mco/templates/default/activemq.xml.erb /etc/activemq/activemq.xml
sudo service activemq restart
