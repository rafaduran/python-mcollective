#!/usr/bin/env python

import unittest
import mcollective
from mcollective import SimpleRPC, Config
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

    def test_configparse(self):
        rpc = SimpleRPC(
            agent='foo',
            action='bar',
            config=TEST_CFG,
            autoconnect=False,
        )
        self.assertEqual(
            '/topic/mcollective.foo.command',
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
                '127.0.0.1',
                6163,
            )
            rpc.stomp_client.connect.assert_called_with(
                'user',
                'pass',
            )

{':agent': 'rpcutil',
 ':body': {':action': 'daemon_stats',
           ':agent': 'rpcutil',
           ':caller': 'cert=icinga-public',
           ':data': {':process_results': True}},
 ':callerid': 'cert=icinga-public',
 ':collective': 'mcollective',
 ':filter': {'agent': ['rpcutil'],
             'cf_class': [],
             'fact': [],
             'identity': ['svs6']},
 ':hash': 'P6OZ/MwKuCV+x6zHO/KtMIAyluGSrNqed2uL2R/fkAJXI0eFANoc8eDb5l8E\nhvvFdMEzw0lH7k7tiHVOouWQEIVhaMFImYDjtK7qeXxbb4u5ub/XL7w5mx+F\nOpBQnKv74NUvhrYf9ANTp7raTYOWX6OSZrSuOBMM5wYofcrhIcVQLziCHRlP\nRUkS5T6GTSEo7VCiLsprCXmfPcJA/DAqjyjDIGpUX7Xt3dB4w8ISaNo73Ys7\nvp9toN47D3S6d/y0J6WB+C/fDIbf3LFzLwoSvrV7kt3ynhxew1K+o0SXPxdo\nlaTPSJcDEV1101nz5DULdavq519byvqsJ9jYx25Nrg==\n',
 ':msgtarget': '/topic/mcollectivemcollective.rpcutil.command',
 ':msgtime': 1315312266,
 ':requestid': 'eb8d0f6419108ad512e43b9aaaf922a8',
 ':senderid': 'icinga'}


def sign(self, private_key, certificate_name, sender_id='python'):
        '''Sign the body of the message.

        :param private_key: an RSA object with a private key loaded.
        :type private_key: M2Crypto.RSA.RSA
        :param certificate_name: the name of the matching cert (as stored on the agents).
        :type certificate_name: str'''
        self.request[":callerid"] = 'cert=%s' % certificate_name
        self.request[":senderid"] = sender_id
        hashed_signature = private_key.sign(sha1(self.body).digest(), 'sha1')
        self.request[':hash'] = hashed_signature.encode('base64').replace("\n", "").strip()