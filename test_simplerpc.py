#!/usr/bin/env python

import unittest
from mcollective import SimpleRPC

class TestSimpleRPC(unittest.TestCase):

    def test_init(self):
        rpc = SimpleRPC(
            agent='foo',
            action='bar',
        )
        self.assertEqual(
            'foo',
            rpc.agent,
        )
        self.assertEqual(
            'bar',
            rpc.action,
        )