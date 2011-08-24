#!/usr/bin/env python

import unittest
from mcollective import Config

class TestConfig(unittest.TestCase):

    def test_init(self):
        c = Config()
        self.assertEqual('/etc/mcollective/client.cfg', c.configfile)


if __name__ == '__main__':
    unittest.main()
