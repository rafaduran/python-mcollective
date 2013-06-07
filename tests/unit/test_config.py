#!/usr/bin/env python
import io
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mcollective import Config

from .. import base

TEST_CFG = base.TEST_CFG


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
        fixtures_path = os.path.join(base.ROOT, 'fixtures')
        self.assertEqual(
            '{path}/testkey-private.pem'.format(path=fixtures_path),
            self.conf.pluginconf['ssl_client_private']
        )
        self.assertEqual(
            '{path}/testkey-public.pem'.format(path=fixtures_path),
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
            base.DEFAULT_CTXT['maincollective'],
            self.conf.main_collective,
        )

    def test_collectives(self):
        self.assertListEqual(base.DEFAULT_CTXT['collectives'],
                             self.conf.collectives)

    def test_stomp_config(self):
        connector = base.DEFAULT_CTXT['connector']
        self.assertEqual(self.conf.connector, connector['name'])
        for key, expected in connector['options'].items():
            value = self.conf.pluginconf['{name}.{key}'.format(
                name=connector['name'],
                key=key)]

            assert expected == value


if __name__ == '__main__':
    unittest.main()
