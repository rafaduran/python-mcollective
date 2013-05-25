# coding: utf-8
import os

import jinja2

ROOT = os.path.abspath(os.path.join(__file__, '..'))
DEFAULT_CTXT = {
    'topic': 'topic',
    'collectives': ['mcollective', 'sub1', 'sub2'],
    'maincollective': 'mcollective',
    'root': ROOT,
    'loglevel': 'debug',
    'daemonize': 0,
    'identity': 'mco1',
    'securityprovider': {
        'name': 'ssl',
        'options': {
            'ssl_server_public': 'mcserver-public.pem',
            'ssl_client_private': '{root}/fixtures/testkey-private.pem'.format(
                root=ROOT),
            'ssl_client_public': '{root}/fixtures/testkey-public.pem'.format(
                root=ROOT),
            'ssl_serializer': 'yaml',
        }
    },
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
TEST_CFG = os.path.join(ROOT, 'server.cfg')


def get_template(name, package=__package__):
    env = jinja2.Environment(loader=jinja2.PackageLoader(package, 'templates'))
    return env.get_template(name)


def configfile():
    with open(TEST_CFG, 'wt') as cfg:
        cfg.write(get_template('server.cfg.jinja').render(DEFAULT_CTXT))
    return TEST_CFG
