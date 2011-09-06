from yaml import load, safe_dump
from time import time, sleep
from hashlib import sha1
from os.path import exists
from stompy.simple import Client
from M2Crypto.RSA import load_key

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


class SimpleRPC(object):

    def __init__(self, agent, action, config=None, stomp_client=None, autoconnect=True, **kwargs):
        self.agent = agent
        self.action = action
        self.config = config or Config()
        self.params = kwargs
        self.stomp_target = '%s.%s.command' % (config.topicprefix, agent)
        self.stomp_target_reply = '%s.%s.reply' % (config.topicprefix, agent)
        self.stomp_client = stomp_client
        if autoconnect and not stomp_client:
            self.connect_stomp()

    def connect_stomp(self):
        self.stomp_client = Client(
            self.config.pluginconf['stomp.host'],
            int(self.config.pluginconf['stomp.port']),
        )
        self.stomp_client.connect(
            self.config.pluginconf['stomp.user'],
            self.config.pluginconf['stomp.password'],
        )


class Signer(object):

    def __init__(self, private_key_path, caller_id):
        self.private_key = load_key(private_key_path)
        self.caller_id = 'cert=' + caller_id

    def sign(self, message):
        message.request[":callerid"] = self.caller_id
        hashed_signature = self.private_key.sign(sha1(message.body).digest(), 'sha1')
        message.request[':hash'] = hashed_signature.encode('base64').replace("\n", "").strip()

        