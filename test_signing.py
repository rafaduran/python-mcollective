#!/usr/bin/env python

import unittest
from mcollective import Signer
from os.path import dirname, join
from M2Crypto.RSA import RSA

PRIVATE_KEY = join(dirname(__file__), 'testkey.pem')


class TestSigning(unittest.TestCase):

    def test_init(self):
        s = Signer(
            PRIVATE_KEY,
            'test-public',
        )
        self.assertIsInstance(
            s.private_key,
            RSA,
        )
        self.assertEqual(
            'cert=test-public',
            s.caller_id,
        )