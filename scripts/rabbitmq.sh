#!/usr/bin/env bash
set -eu
service rabbitmq-server start  # chef stops it
rabbitmq-plugins enable rabbitmq_stomp
# Each MCollective collective requires two exchanges, direct and broadcast
# In this case just `mcollective` collective
`dirname $0`/rabbitmqadmin declare exchange name=mcollective_directed type=direct
`dirname $0`/rabbitmqadmin declare exchange name=mcollective_broadcast type=topic
service rabbitmq-server stop  # stop it again
