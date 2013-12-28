#!/usr/bin/env bash
set -eu
ROOT=`dirname $0`

sudo apt-get install python-pip -y
pip install requests --use-mirrors
sudo rabbitmq-plugins enable rabbitmq_stomp
${ROOT}/rabbitmq.py
sudo service rabbitmq-server restart  # so changes make effect
