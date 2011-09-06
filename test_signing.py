#!/usr/bin/env python

import unittest
from mcollective import Signer, Message
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

    def test_sign(self):
        m = Message('Testing123')
        s = Signer(
            PRIVATE_KEY,
            'test-public',
        )
        s.sign(m)
        self.assertEqual(
            'cert=test-public',
            m.request[':callerid'],
        )
        self.assertEqual(
            'MVLizyhmBLtvw0SpOZNazatmXhSAjeBH0BvuRlDZrdn2mAwpWBxoNwKvsT8V/01NpBodhxosBeNeBeg/7X/T7g==',
            m.request[':hash'],
        )