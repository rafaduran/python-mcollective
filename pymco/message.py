'''pymco messaging objects'''
import collections
import hashlib
import time

import six

from . import exc

class Filter(object):
    '''Provides MCollective filters for pymco.'''
    def __init__(self):
        self._filter = {
            'cf_class': [],
            'agent': [],
            'fact': [],
            'identity': [],
        }

    def add_cfclass(self, klass):
        '''Adds new classes/recipes/cookbooks/roles applied by your
        configuration management system.'''
        self._filter['cf_class'].append(klass)
        return self

    def add_agent(self, agent):
        '''Adds new agents'''
        self._filter['agent'].append(agent)
        return self

    def add_fact(self, fact, value, operator=None):
        '''Adds new facts'''
        toappend = {':fact': fact, ':value': value}
        if operator:
            if not operator in ('==', '=~', '<=', '=>', '>=', '=<', '>', '<',
                                '!='):
                raise exc.BadFilterFactOperator(
                    'Unsuppoerted operator {0}'.format(operator))
            toappend[':operator'] = operator
        self._filter['fact'].append(toappend)
        return self

    def add_identity(self, identity):
        '''Adds new identities'''
        self._filter['identity'].append(identity)
        return self

    def as_dict(self):
        '''Return dict representation for current filter'''
        return self._filter


class Message(collections.Mapping):
    '''Provides MCollective messages for pymco.'''
    def __init__(self, body, agent, config, **kwargs):
        self._message = {}
        try:
            self._message['senderid'] = config['identity']
            self._message['collective'] = kwargs.get('collective', None) or \
                    config['main_collective']
        except KeyError as error:
            raise exc.ImproperlyConfigured(error)
        self._message['msgtime'] = int(time.time())
        self._message['ttl'] = kwargs.get('ttl', None) or \
                config.getint('ttl', default=60)
        self._message['requestid'] = hashlib.sha1(
            str(self._message['msgtime'])).hexdigest()
        self._message['body'] = body
        self._message['agent'] = agent

    def __len__(self):
        return len(self._message)

    def __iter__(self):
        return six.iterkeys(self._message)

    def __getitem__(self, key):
        return self._message[key]
