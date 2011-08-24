from yaml import load, safe_dump
from time import time, sleep
from hashlib import sha1
from os.path import exists

__version__ = '0.2'

class AlreadySentException(Exception):
    pass


class Config(object):

    def __init__(self, configfile='/etc/mcollective/client.cfg', parse=True):
        '''MCollective Configuration State'''
        self.configfile = configfile
        self.pluginconf = {}
        self.topicprefix = ''

        if parse:
            self.parse_config()

    def _handle_plugin(self, line):
        k, v = [v.strip() for v in line.split('=')]
        k = k.split('.', 1)[1]
        self.pluginconf[k] = v

    def _handle_default(self, line):
        k, v = [v.strip() for v in line.split('=')]
        setattr(self, k, v)

    def parse_config(self):
        if not exists(self.configfile):
            raise ValueError('Config file %s doesnt exist' % self.configfile)
        lines = open(self.configfile).readlines()
        # Remove empty lines, lowercase everything
        lines = [l.lower() for l in lines if l]
        dispatch = {
            'plugin.' : self._handle_plugin,
            'topicprefix' : self._handle_default
        }
        for l in lines:
            for k in dispatch.keys():
                if l.startswith(k):
                    dispatch[k](l)
                    break


class Filter(object):

    def __init__(self, cf_class='', agent='', identity=''):
        '''Filter which nodes respond to a message
     
        :param cf_class: Match classes applied by puppet etc
        :param agent: Match the list of agents
        :param identity: Match the identity configured in the configuration file
        '''
        self.cf_class = cf_class
        self.agent = agent
        self.identity = identity
        self.fact = []

    def add_fact(self, name, value):
        '''Add a fact to the collection of filters

        :param name: Name of the fact
        :param value: Value to match
        '''
        self.fact.append({':fact' : name, ':value' : value})

    def dump(self):
        '''Dump this filter into a dictionary
        
        :rtype: Dictionary of filter parameters'''
        return {
            'cf_class' : self.cf_class and [self.cf_class] or [],
            'agent' : self.agent and [self.agent] or [],
            'identity' : self.identity and [self.identity] or [],
            'fact' : self.fact,
        }


class Message(object):

    def __init__(self, body, filter_=None, target='rpcutil'):
        '''Create a new message.
        
        :param body: Correctly encoded RPC message.
        :type body: dict
        :param filter_: An mcollective.Filter instance
        :param stomp_client: Open connection to STOMP server
        :param prefix: MCollective prefix
        :param target: MCollective target'''
        self.target = target
        self.rid = sha1(str(time())).hexdigest()
        self.sent = False
        r = dict()
        r[':msgtime'] = int(time())
        r[':filter'] = (filter_ or Filter()).dump()
        r[":requestid"] = self.rid
        r[":msgtarget"] = self.target
        self.body = safe_dump(body, explicit_start=True, explicit_end=False, default_flow_style=False)
        self.request = r