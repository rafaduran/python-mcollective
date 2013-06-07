# coding: utf-8
import os

import jinja2

ROOT = os.path.abspath(os.path.join(__file__, '..'))
DEFAULT_CTXT = {
    'topic': 'topic',
    'collectives': ['mcollective', 'sub1'],
    'maincollective': 'mcollective',
    'root': ROOT,
    'loglevel': 'debug',
    'daemonize': 0,
    'identity': 'mco1',
    'securityprovider': 'none',
    'connector': {
        'name': 'activemq',
        'options': {
            'pool.size': '1',
            'pool.1.host': 'localhost',
            'pool.1.port': '6163',
            'pool.1.user': 'mcollective',
            'pool.1.password': 'secret',
            'pool.1.ssl': 'false',
        },
    },
}


def get_template(name, package=__package__):
    env = jinja2.Environment(loader=jinja2.PackageLoader(package, 'templates'))
    return env.get_template(name)
