#!/usr/bin/env bash
set -eu
ROOT=`dirname $0`

sudo apt-get install python-pip -y
pip install requests --use-mirrors
sudo rabbitmq-plugins enable rabbitmq_stomp
${ROOT}/rabbitmq.py
sudo cp ${ROOT}/../extra_cookbooks/rabbitmq_mco/templates/default/rabbitmq.config.erb \
    /etc/rabbitmq/rabbitmq.config
sudo sed -i 's/<%= node.rabbitmq.high_memory_watermark %>/0.04/' /etc/rabbitmq/rabbitmq.config
sudo cp ${ROOT}/../extra_cookbooks/rabbitmq_mco/templates/default/ca.pem \
    /etc/rabbitmq/ca.pem
sudo cp ${ROOT}/../extra_cookbooks/rabbitmq_mco/templates/default/cert.pem \
    /etc/rabbitmq/cert.pem
sudo cp ${ROOT}/../extra_cookbooks/rabbitmq_mco/templates/default/key.pem \
    /etc/rabbitmq/key.pem
sudo service rabbitmq-server restart  # so changes make effect
