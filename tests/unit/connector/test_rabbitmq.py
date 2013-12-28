"""Tests for pymco.rabbitmq"""
import pytest

import pymco.config
from pymco.connector import rabbitmq
from pymco.test.utils import mock

CONFIGSTR = """collectives = mcollective
main_collective = mcollective
libdir = tests/integration/vendor/plugins
logger_type = console
loglevel = debug
daemonize = 0
identity = mco1

# Plugins
securityprovider = none

direct_addressing = yes
direct_addressing_threshold = 5

connector = rabbitmq
plugin.rabbitmq.vhost = /mcollective
plugin.rabbitmq.pool.size = 1
plugin.rabbitmq.pool.1.host = localhost
plugin.rabbitmq.pool.1.port = 61613
plugin.rabbitmq.pool.1.user = mcollective
plugin.rabbitmq.pool.1.password = marionette

factsource = yaml
plugin.yaml = tests/fixtures/facts.yaml
"""


@pytest.fixture
def config():
    return pymco.config.Config.from_configstr(CONFIGSTR)


@pytest.fixture
def connector(config, conn_mock):
    return rabbitmq.RabbitMQConnector(config=config, connection=conn_mock)


def test_get_target(connector):
    assert connector.get_target(agent='agent', collective='collective') == (
        '/exchange/collective_broadcast/agent')


def test_get_reply_target(connector):
    assert connector.get_reply_target(agent='agent', collective='collective') == (
        '/queue/collective_reply_agent')


@mock.patch('stomp.Connection')
def test_default_connection(conn_class, config):
    rabbitmq.RabbitMQConnector(config=config)
    conn_class.assert_called_once_with(
        host_and_ports=config.get_host_and_ports(),
        vhost=config['plugin.rabbitmq.vhost'],
    )
