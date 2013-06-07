#!/usr/bin/env python

try:
    import unittest2 as unittest
except ImportError:
    import unittest
import mcollective
from os.path import dirname, join
from M2Crypto.RSA import RSA

PRIVATE_KEY = join(dirname(__file__), '../fixtures/testkey-private.pem')
PUBLIC_KEY = join(dirname(__file__), '../fixtures/testkey-public.pem')


class TestSigning(unittest.TestCase):
    def setUp(self):
        self.conf = mcollective.Config(parse=False)
        self.conf.pluginconf['ssl_client_private'] = PRIVATE_KEY
        self.conf.pluginconf['ssl_client_public'] = PUBLIC_KEY
        self.signer = mcollective.SSLSigner(self.conf)

    def test_init(self):
        self.assertIsInstance(
            self.signer.private_key,
            RSA,
        )
        self.assertEqual(
            'cert=testkey-public',
            self.signer.caller_id,
        )

    def test_sign(self):
        m = mcollective.Message('Testing123', '/topic/foo')
        self.signer.sign(m)
        self.assertEqual(
            'cert=testkey-public',
            m.request[':callerid'],
        )
        self.assertEqual(
            "hWBxnfroy5XJmnl25UnnQGjJjbkkG248vnzj5kxdh5dKLX8QZpEquV5BLul/uovz"
            "L9D47SWREc7cVcIcL8WBLQ==",
            m.request[':hash'],
        )

if __name__ == '__main__':
    unittest.main()
