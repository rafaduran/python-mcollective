#!/usr/bin/env bash

set -eu

sudo chef-solo -c chef/solo.rb -j chef/dna.json
sudo /etc/init.d/rabbitmq-server start
sudo TRAVIS=true scripts/rabbitmq.sh
sudo scripts/activemq.sh
