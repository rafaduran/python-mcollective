#!/usr/bin/env python

import unittest
import mcollective
from mcollective import SimpleRPC, Config, SimpleRPCProxy, SimpleRPCProxyAgent
from test_config import TEST_CFG
import mock

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
            mcollective.Signer
        )

    def test_configparse(self):
        rpc = SimpleRPC(
            agent='foo',
            action='bar',
            config=TEST_CFG,
            autoconnect=False,
        )
        self.assertEqual(
            '/topic/mcollectivemcollective.foo.command',
            rpc.stomp_target,
        )
        self.assertEqual(
            '/topic/mcollectivemcollective.foo.reply',
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
                '127.0.0.1',
                6163,
            )
            rpc.stomp_client.connect.assert_called_with(
                'user',
                'pass',
            )

    def test_send_message(self):
        with mock.patch('mcollective.Client') as mocked:
            rpc = SimpleRPC(
                agent='foo',
                action='bar',
                config=TEST_CFG,
            )
            rpc.send(ham='eggs')
            put = rpc.stomp_client.put
            put.assert_called()