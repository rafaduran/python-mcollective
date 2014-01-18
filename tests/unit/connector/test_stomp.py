"""
Tests for StompConnector
"""
from __future__ import absolute_import
import pytest

from pymco.connector import stomp
from pymco.test.utils import mock

CONFIGSTR = '''
topicprefix = /topic/
collectives = mcollective
main_collective = mcollective
libdir = /path/to/plugins
logfile = /path/to/mcollective.log
loglevel = debug
daemonize = 0
identity = mco1

# Plugins
securityprovider = none

direct_addressing = yes
direct_addressing_threshold = 5

connector = stomp
plugin.stomp.host = localhost
plugin.stomp.password = guest
plugin.stomp.port = 61613
plugin.stomp.user = guest

factsource = yaml
plugin.yaml = /path/to/facts.yaml
'''


@pytest.fixture
def config():
    from pymco import config
    return config.Config.from_configstr(configstr=CONFIGSTR)


@pytest.fixture
def connector(config, conn_mock):
    return stomp.StompConnector(config, connection=conn_mock)


@mock.patch('stomp.Connection')
def test_default_connection(conn, config):
    connector = stomp.StompConnector(config=config)
    assert connector.connection is conn.return_value
    conn.assert_called_once_with(host_and_ports=[('localhost', 61613)])


def test_get_target(connector, config):
    assert connector.get_target(collective='collective', agent='agent') == (
        '{0}collective.agent.command'.format(config['topicprefix'])
    )


def test_get_reply_target(connector, config):
    assert connector.get_reply_target(collective='collective', agent='agent') == (
        '{0}collective.agent.reply'.format(config['topicprefix'])
    )
