'''pymco messaging objects'''
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
