#!/usr/bin/env bash
set -eu
ROOT=`dirname $0`

sudo apt-get install python-pip -y
pip install requests --use-mirrors
sudo rabbitmq-plugins enable rabbitmq_stomp
${ROOT}/rabbitmq.py
sudo cp ${ROOT}/extra_cookbooks/rabbitmq_mco/templates/default/ca.pem \
    /opt/rabbitmq/ca.pem
sudo cp ${ROOT}/extra_cookbooks/rabbitmq_mco/templates/default/cert.pem \
    /opt/rabbitmq/cert.pem
sudo cp ${ROOT}/extra_cookbooks/rabbitmq_mco/templates/default/key.pem \
    /opt/rabbitmq/key.pem
sudo service rabbitmq-server restart  # so changes make effect
