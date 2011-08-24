#!/usr/bin/env python

import unittest
from mcollective import Message, Filter

EMPTY_FILTER = Filter()

class TestMessage(unittest.TestCase):

    def test_init(self):
        m = Message({':foo' : 'bar'})
        self.assertEqual(
            EMPTY_FILTER.dump(),
            m.request[':filter'],
            "Default filter not empty",
        )
        self.assertEqual(
            '---\n:foo: bar\n',
            m.body
        )
        self.assertEqual(
            'rpcutil',
            m.target,
        )
        self.assertFalse(m.sent)

    def test_custom_filter(self):
        f = Filter(identity='foo.bar.baz.com')
        m = Message(
            body={':foo' : 'bar'},
            filter_=f,
        )
        self.assertEqual(
            f.dump(),
            m.request[':filter'],
            "Custom filter not correct",
        )