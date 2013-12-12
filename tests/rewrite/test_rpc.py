"""Tests for pymco.rpc"""
from .. import base


def test_simple_action_get_target(simple_action):
    assert simple_action.get_target() == (
        '/topic/mcollective.{0}.command'.format(base.MSG['agent'])
    )


def test_simple_action_get_reply_target(simple_action):
    assert simple_action.get_reply_target() == (
        '/topic/mcollective.{0}.reply'.format(base.MSG['agent'])
    )


def test_simple_action_call__connect(simple_action, connector):
    simple_action.call()
    connector.connect.assert_called_with(wait=True)


def test_simple_action_call__subscribe_to_reply(simple_action, connector):
    simple_action.call()
    reply_target = simple_action.get_reply_target()
    connector.subscribe.assert_called_with(destination=reply_target)


def test_simple_action_call__send_msg(simple_action, connector, msg):
    simple_action.call()
    target = simple_action.get_target()
    connector.send.assert_called_with(msg, target)


def test_simple_action_call__disconnect(simple_action, connector):
    simple_action.call()
    connector.disconnect.assert_called_with()


def test_simple_action_call__receive_default_timeout(simple_action, connector):
    simple_action.call()
    connector.receive.assert_called_once_with(timeout=5)


def test_simple_action_call__receive_custom_timeout(simple_action, connector):
    simple_action.call(timeout=10)
    connector.receive.assert_called_once_with(timeout=10)
