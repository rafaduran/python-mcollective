#!/usr/bin/env python

import unittest
from mcollective import Filter

class TestFilter(unittest.TestCase):

    def test_init(self):
        f = Filter()
        self.assertEqual(f.cf_class, '')
        self.assertEqual(f.agent, '')
        self.assertEqual(f.identity, '')
        self.assertEqual(f.fact, [])

    def test_cf_class(self):
        f = Filter(cf_class='foo::bar')
        self.assertEqual(f.cf_class, 'foo::bar')
        self.assertEqual(
            f.dump()['cf_class'],
            ['foo::bar'],
        )

    def test_agent(self):
        f = Filter(agent='smith')
        self.assertEqual(f.agent, 'smith')
        self.assertEqual(
            f.dump()['agent'],
            ['smith'],
        )

    def test_identity(self):
        f = Filter(identity='the.bourne')
        self.assertEqual(f.identity, 'the.bourne')
        self.assertEqual(
            f.dump()['identity'],
            ['the.bourne'],
        )

    def test_fact(self):
        f = Filter()
        f.add_fact('country', 'uk')
        self.assertEqual(f.fact, [{'country' : 'uk'}])
        self.assertEqual(
            f.dump()['fact'],
            [{'country' : 'uk'}],
        )

    def test_add_multiple_facts(self):
        f = Filter()
        f.add_fact('country', 'us')
        self.assertEqual(f.fact, [{'country' : 'us'}])
        f.add_fact('processorcount', '4')
        self.assertEqual(f.fact,[
            {'country' : 'us'},
            {'processorcount' : '4'},
        ])
        self.assertEqual(f.dump()['fact'], f.fact)

    def test_empty_dump(self):
        f = Filter()
        d = f.dump()
        self.assertEqual(d, {
            'cf_class' : [],
            'agent' : [],
            'identity' : [],
            'fact' : [],
        })

    def test_full_dump(self):
        f = Filter(
            cf_class='foo::bar',
            agent='smith',
            identity='the.bourne',
        )
        f.add_fact('country', 'uk')
        f.add_fact('processorcount', '4')
        d = f.dump()
        self.assertEqual(d, {
            'cf_class' : ['foo::bar'],
            'agent' : ['smith'],
            'identity' : ['the.bourne'],
            'fact' : [
                {'country' : 'uk'},
                {'processorcount' : '4'},
            ],
        })


if __name__ == '__main__':
    unittest.main()
