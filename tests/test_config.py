#!/usr/bin/env python

from os.path import dirname
from os.path import join
import unittest
from mcollective import Config

TEST_CFG = join(dirname(__file__), 'fixtures/test_client.cfg')

class TestConfig(unittest.TestCase):
    def setUp(self):
        super(TestConfig, self).setUp()
        self.conf = Config(TEST_CFG)

    def test_init(self):
        c = Config(parse=False)
        self.assertEqual('/etc/mcollective/client.cfg', c.configfile)
        self.assertEqual({}, c.pluginconf)
        self.assertEqual('/topic/', c.topicprefix)


    def test_different_config_file(self):
        self.assertEqual(TEST_CFG, self.conf.configfile)

    def test_ssl_paths(self):
        self.assertEqual(
            'tests/fixtures/testkey-private.pem',
            self.conf.pluginconf['ssl_client_private']
        )
        self.assertEqual(
            'tests/fixtures/testkey-public.pem',
            self.conf.pluginconf['ssl_client_public']
        )
        self.assertEqual(
            'yaml',
            self.conf.pluginconf['ssl_serializer']
        )
        self.assertEqual(
            'mcserver-public.pem',
            self.conf.pluginconf['ssl_server_public']
        )

    def test_topicprefix(self):
        self.assertEqual('/topic/', self.conf.topicprefix)

    def test_maincollective(self):
        self.assertEqual(
            'mcollective',
            self.conf.main_collective,
        )

    def test_collectives(self):
        self.assertListEqual(['mcollective'], self.conf.collectives)

    def test_stomp_config(self):
        self.assertEqual(
            'localhost',
            self.conf.pluginconf['stomp.host']
        )
        self.assertEqual(
            '61613',
            self.conf.pluginconf['stomp.port']
        )
        self.assertEqual(
            'mcollective',
            self.conf.pluginconf['stomp.user']
        )
        self.assertEqual(
            'secret',
            self.conf.pluginconf['stomp.password']
        )


if __name__ == '__main__':
    unittest.main()
