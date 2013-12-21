"""Tests for pymco.rpc"""
from .. import base

import mock

from pymco import rpc


def test_simple_action_get_target(simple_action):
    assert simple_action.get_target() == (
        '/topic/mcollective.{0}.command'.format(base.MSG['agent'])
    )


def test_simple_action_get_target__custom_collective(config, msg):
    simple_action = rpc.SimpleAction(agent=base.MSG['agent'],
                                     config=config,
                                     msg=msg,
                                     collective='foocollective')
    assert simple_action.get_target() == (
        '/topic/foocollective.{0}.command'.format(base.MSG['agent'])
    )


def test_simple_action_get_reply_target(simple_action):
    assert simple_action.get_reply_target() == (
        '/topic/mcollective.{0}.reply'.format(base.MSG['agent'])
    )


def test_simple_action_get_reply_target__custom_collective(config, msg):
    simple_action = rpc.SimpleAction(agent=base.MSG['agent'],
                                     config=config,
                                     msg=msg,
                                     collective='foocollective')
    assert simple_action.get_reply_target() == (
        '/topic/foocollective.{0}.reply'.format(base.MSG['agent'])
    )


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
        connector.send.assert_called_with(msg, target)

    def test_disconnects(self, connector, simple_action):
        simple_action.call()
        connector.disconnect.assert_called_with()

    def test_receives__default_timeout(self, connector, simple_action):
        simple_action.call()
        connector.receive.assert_called_once_with(timeout=5)

    def test_receives__custom_timeout(self, connector, simple_action):
        simple_action.call(timeout=10)
        connector.receive.assert_called_once_with(timeout=10)
