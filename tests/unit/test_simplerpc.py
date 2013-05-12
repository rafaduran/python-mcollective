#!/usr/bin/env python
import unittest
import mcollective
from mcollective import Config, SimpleRPCAction as SimpleRPC
from test_config import TEST_CFG
import mock
import stompy

TEST_CFG = Config(TEST_CFG)


class TestSimpleRPC(unittest.TestCase):
    def test_init(self):
        rpc = SimpleRPC(
            agent='foo',
            action='bar',
            config=TEST_CFG,
            autoconnect=False,
        )
        self.assertEqual(
            'foo',
            rpc.agent,
        )
        self.assertEqual(
            'bar',
            rpc.action,
        )
        self.assertEqual(
            TEST_CFG,
            rpc.config,
        )
        self.assertEqual(
            {},
            rpc.params,
        )
        self.assertIsInstance(
            rpc.signer,
            mcollective.SSLSigner
        )

    def test_configparse(self):
        rpc = SimpleRPC(
            agent='foo',
            action='bar',
            config=TEST_CFG,
            autoconnect=False,
        )
        self.assertEqual(
            '/topic/mcollective.foo.agent',
            rpc.stomp_target,
        )
        self.assertEqual(
            '/topic/mcollective.foo.reply',
            rpc.stomp_target_reply,
        )

    def test_connect_stomp(self):
        with mock.patch('mcollective.Client') as mocked:
            rpc = SimpleRPC(
                agent='foo',
                action='bar',
                config=TEST_CFG,
            )
            mocked.assert_called_with(
                'localhost',
                61613,
            )
            rpc.stomp_client.connect.assert_called_with(
                'mcollective',
                'secret',
            )

    def test_send_message(self):

        with mock.patch('mcollective.Client') as mocked:
            instance = mocked.return_value
            instance.get_nowait = mock.Mock(side_effect=stompy.Empty)
            rpc = SimpleRPC(
                agent='foo',
                action='bar',
                config=TEST_CFG,
            )
            rpc.send(ham='eggs')
            put = rpc.stomp_client.put
            put.assert_called()


if __name__ == '__main__':
    unittest.main()
