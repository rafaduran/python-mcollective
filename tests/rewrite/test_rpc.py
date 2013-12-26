"""Tests for pymco.rpc"""
from .. import base

import mock
import pytest

from pymco import rpc


@pytest.fixture
def simple_action(config, msg):
    return rpc.SimpleAction(agent=base.MSG['agent'],
                            config=config,
                            msg=msg)


def test_custom_collective(config, msg):
    simple_action = rpc.SimpleAction(agent=base.MSG['agent'],
                                     config=config,
                                     msg=msg,
                                     collective='foocollective')
    assert simple_action.collective == 'foocollective'


@mock.patch('pymco.config.Config.get_connector')
def test_simple_action_connector___gets_connector(get_connector, simple_action):
    assert simple_action.connector == get_connector.return_value


@mock.patch('pymco.config.Config.get_connector')
def test_simple_action_connector___caches_connector(get_connector, simple_action):
    connector = mock.Mock()
    simple_action._connector = connector
    assert simple_action.connector == connector
    assert get_connector.called is False


@mock.patch('pymco.rpc.SimpleAction.connector')
class TestSimpleActionCall():
    def test_it_connects(self, connector, simple_action):
        simple_action.call()
        connector.connect.assert_called_with(wait=True)

    def test_it_subscribes_to_reply(self, connector, simple_action):
        simple_action.call()
        reply_target = simple_action.get_reply_target()
        connector.subscribe.assert_called_with(
            destination=reply_target)

    def test_sends_msg(self, connector, simple_action, msg):
        simple_action.call()
        target = simple_action.get_target()
        reply_target = simple_action.get_reply_target()
        connector.send.assert_called_with(msg,
                                          target,
                                          **{'reply-to': reply_target})

    def test_disconnects(self, connector, simple_action):
        simple_action.call()
        connector.disconnect.assert_called_with()

    def test_receives__default_timeout(self, connector, simple_action):
        simple_action.call()
        connector.receive.assert_called_once_with(timeout=5)

    def test_receives__custom_timeout(self, connector, simple_action):
        simple_action.call(timeout=10)
        connector.receive.assert_called_once_with(timeout=10)

    def test_get_target_delegates_connector(self, connector, simple_action):
        assert simple_action.get_target() == connector.get_target.return_value
        connector.get_target.assert_called_once_with(
            collective=simple_action.collective,
            agent=simple_action.agent,
        )

    def test_get_reply_target_delegates_connector(self, connector, simple_action):
        assert (simple_action.get_reply_target() ==
                connector.get_reply_target.return_value)
        connector.get_reply_target.assert_called_once_with(
            collective=simple_action.collective,
            agent=simple_action.agent,
        )
