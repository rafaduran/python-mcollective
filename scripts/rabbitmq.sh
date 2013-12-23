#!/usr/bin/env bash
set -eu
sudo rabbitmq-plugins enable rabbitmq_stomp
`dirname $0`/rabbitmqadmin declare vhost name=/mcollective
`dirname $0`/rabbitmqadmin declare user name=mcollective password=marionette tags=
`dirname $0`/rabbitmqadmin declare user name=admin password=marionette tags=administrator
`dirname $0`/rabbitmqadmin declare permission vhost=/mcollective user=mcollective configure='.*' write='.*' read='.*'
`dirname $0`/rabbitmqadmin declare permission vhost=/mcollective user=admin configure='.*' write='.*' read='.*'

# Each MCollective collective requires two exchanges, direct and broadcast
# In this case just `mcollective` collective
for collective in mcollective ; do
    `dirname $0`/rabbitmqadmin declare exchange --user=admin --password=marionette --vhost=/mcollective name=${collective}_broadcast type=topic
    `dirname $0`/rabbitmqadmin declare exchange --user=admin --password=marionette --vhost=/mcollective name=${collective}_directed type=direct
done

sudo service rabbitmq-server restart  # so changes make effect
