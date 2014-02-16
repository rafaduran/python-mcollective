"""Tests for pymco.connector.activemq"""
import pytest


from pymco.connector import activemq
from pymco.test.utils import mock


@pytest.fixture
def connector(config, conn_mock):
    return activemq.ActiveMQConnector(config=config, connection=conn_mock)


def test_get_target(connector):
    assert connector.get_target(collective='collective', agent='agent') == (
        '/topic/collective.agent.agent')


@mock.patch('os.getpid')
def test_get_reply_target(getpid, connector):
    getpid.return_value = 12345
    assert connector.get_reply_target(collective='collective', agent='agent') == (
        '/queue/collective.reply.mco1_12345')


@mock.patch('pymco.connector.Connector.security',
            new_callable=mock.PropertyMock)
def test_send__msg_priority(security, connector, conn_mock, config):
    config.config['plugin.activemq.priority'] = 4
    connector.send('foo', 'spam')
    conn_mock.send.assert_called_once_with(
        body=security.return_value.encode('foo'),
        destination='spam',
        priority=4,
    )
