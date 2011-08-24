#!/usr/bin/env python

from os.path import dirname
from os.path import join
import unittest
from mcollective import Config

TEST_CFG = join(dirname(__file__), 'test_client.cfg')

class TestConfig(unittest.TestCase):

    def test_init(self):
        c = Config(parse=False)
        self.assertEqual('/etc/mcollective/client.cfg', c.configfile)
        self.assertEqual({}, c.pluginconf)
        self.assertEqual('', c.topicprefix)


    def test_different_config_file(self):
        c = Config(TEST_CFG)
        self.assertEqual(TEST_CFG, c.configfile)

    def test_ssl_paths(self):
        c = Config(TEST_CFG)
        self.assertEqual(
            '/tmp/test-private.pem',
            c.pluginconf['ssl_client_private']
        )
        self.assertEqual(
            '/tmp/test-public.pem',
            c.pluginconf['ssl_client_public']
        )
        self.assertEqual(
            'yaml',
            c.pluginconf['ssl_serializer']
        )
        self.assertEqual(
            '/tmp/mcserver-public.pem',
            c.pluginconf['ssl_server_public']
        )

    def test_topicprefix(self):
        c = Config(TEST_CFG)
        self.assertEqual('/topic/mcollective', c.topicprefix)

    def test_stomp_config(self):
        c = Config(TEST_CFG)
        self.assertEqual(
            '127.0.0.1',
            c.pluginconf['stomp.host']
        )
        self.assertEqual(
            '6163',
            c.pluginconf['stomp.port']
        )
        self.assertEqual(
            'user',
            c.pluginconf['stomp.user']
        )
        self.assertEqual(
            'pass',
            c.pluginconf['stomp.password']
        )


if __name__ == '__main__':
    unittest.main()