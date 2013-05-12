#!/usr/bin/env python
import io
import os
import unittest

from mcollective import Config

TEST_CFG = os.path.join(os.path.dirname(__file__),
                        '../fixtures/test_client.cfg')
PATH = os.path.abspath(os.path.dirname(TEST_CFG))

if not os.path.exists(TEST_CFG):
    with io.open(TEST_CFG + '.template', 'rt') as fin:
        with io.open(TEST_CFG, 'wt') as fout:
            contents = fin.read().format(path=PATH)
            fout.write(contents)


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
            '{path}/testkey-private.pem'.format(path=PATH),
            self.conf.pluginconf['ssl_client_private']
        )
        self.assertEqual(
            '{path}/testkey-public.pem'.format(path=PATH),
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
