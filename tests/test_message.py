#!/usr/bin/env python

import unittest
from mcollective import Message, Filter

EMPTY_FILTER = Filter()


class TestMessage(unittest.TestCase):
    def test_init(self):
        m = Message({':foo': 'bar'}, '/topic/foo')
        self.assertEqual(EMPTY_FILTER.dump(),
                         m.request[':filter'],
                         "Default filter not empty",
                         )
        self.assertEqual('\n:foo: bar\n', m.body)

    def test_custom_filter(self):
        f = Filter(identity='foo.bar.baz.com')
        m = Message(body={':foo': 'bar'},
                    target='/topic/foo',
                    filter_=f
                    )
        self.assertEqual(f.dump(),
                         m.request[':filter'],
                         "Custom filter not correct",
                         )


if __name__ == '__main__':
    unittest.main()
