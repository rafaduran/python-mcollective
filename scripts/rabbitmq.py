#!/usr/bin/env python
import functools
import json
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus


import requests

AUTH = ('guest', 'guest')
ADMIN_AUTH = ('admin', 'marionette')
URL = 'http://localhost:15672'
HEADERS = {'content-type': 'application/json'}


def single_resource(resource, **kwargs):
    return requests.put('{0}/api/{1}/{2}'.format(URL,
                                                 resource,
                                                 quote_plus(kwargs['name'])),
                        auth=AUTH,
                        headers=HEADERS,
                        data=json.dumps(kwargs))


def nested_resource(resource, resource_key, nested_key, auth=AUTH, **kwargs):
    url = '{0}/api/{1}/{2}/{3}'.format(URL,
                                       resource,
                                       quote_plus(kwargs[resource_key]),
                                       quote_plus(kwargs[nested_key]))
    return requests.put(url,
                        auth=auth,
                        headers=HEADERS,
                        data=json.dumps(kwargs))


declare_vhost = functools.partial(single_resource, resource='vhosts')
declare_user = functools.partial(single_resource, resource='users')
declare_permission = functools.partial(nested_resource,
                                       resource='permissions',
                                       resource_key='vhost',
                                       nested_key='user')
declare_exchange = functools.partial(nested_resource,
                                     resource='exchanges',
                                     resource_key='vhost',
                                     nested_key='name')


def assert_success(response):
    assert response.status_code in (200, 204)


def main():
    assert_success(declare_vhost(vhost='/', name='/mcollective'))
    assert_success(declare_user(vhost='/',
                                password='marionette',
                                name='mcollective',
                                tags=''))
    assert_success(declare_user(vhost='/',
                                password='marionette',
                                name='admin',
                                tags='administrator'))
    assert_success(declare_permission(write='.*',
                                      vhost='/mcollective',
                                      read='.*',
                                      user='mcollective',
                                      configure='.*'))
    assert_success(declare_permission(write='.*',
                                      vhost='/mcollective',
                                      read='.*',
                                      user='admin',
                                      configure='.*'))
    assert_success(declare_exchange(name='mcollective_broadcast',
                                    auto_delete=False,
                                    vhost="/mcollective",
                                    internal=False,
                                    type="topic",
                                    auth=ADMIN_AUTH,
                                    durable=True))
    assert_success(declare_exchange(name='mcollective_directed',
                                    auto_delete=False,
                                    vhost="/mcollective",
                                    internal=False,
                                    type="direct",
                                    auth=ADMIN_AUTH,
                                    durable=True))


if __name__ == '__main__':
    main()
