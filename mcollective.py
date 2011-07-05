from yaml import load, safe_dump
from time import time, sleep
from hashlib import sha1

__version__ = '0.2'

class AlreadySentException(Exception):
    pass


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
    def __init__(self, body, stomp_client, filter_=None, prefix='mcollective', target='rpcutil'):
        '''Create a new message.
        
        :param body: Correctly encoded RPC message.
        :type body: dict
        :param stomp_client: Open connection to STOMP server
        :param prefix: MCollective prefix
        :param target: MCollective target'''
        self.stomp_client = stomp_client
        self.target = '/topic/%s.%s.command' % (prefix, target)
        self.target_reply = '/topic/%s.%s.reply' % (prefix, target)
        self.rid = sha1(str(time())).hexdigest()
        self.sent = False
        r = dict()
        r[':msgtime'] = int(time())
        r[':filter'] = filter_ or Filter().dump()
        r[":requestid"] = self.rid
        r[":msgtarget"] = self.target
        self.body = safe_dump(body, explicit_start=True, explicit_end=False, default_flow_style=False)
        self.request = r
    
    def subscribe_to_replies(self):
        '''Subscribe to the response topic for this message.
        
        You should run this before sending the message, if you are interested
        in the replies from agents.'''
        self.stomp_client.subscribe(self.target_reply)
    
    def sign(self, private_key, certificate_name, sender_id='python'):
        '''Sign the body of the message.

        :param private_key: an RSA object with a private key loaded.
        :type private_key: M2Crypto.RSA.RSA
        :param certificate_name: the name of the matching cert (as stored on the agents).
        :type certificate_name: str'''
        self.request[":callerid"] = 'cert=%s' % certificate_name
        self.request[":senderid"] = sender_id
        hashed_signature = private_key.sign(sha1(self.body).digest(), 'sha1')
        self.request[':hash'] = hashed_signature.encode('base64').replace("\n", "").strip()

    def send(self, debug=False):
        '''Send the encoded message to the target topic

        :param debug: if true, the message will be printed to standard error.
        :type debug: boolean
        
        You can only send each message once. Subsequent calls will raise :class:`AlreadySentException`'''
        if self.sent:
            raise AlreadySentException()
        data = safe_dump(self.request, explicit_start=True, explicit_end=False)
        body = "\n".join(['  %s' % line for line in self.body.split("\n")])
        data = data + ":body: |\n" + body
        if debug:
            import sys
            print >>sys.stderr, data
        self.stomp_client.put(data, self.target)
        self.sent = True
    
    def collect_results(self):
        '''Collect the results from a previous :func:`Message.send` call.
        
        :rtype: list of STOMP messages which match this object's `:requestid`'''
        results = []
        while True:
            message = None
            try:
                message = self.stomp_client.get_nowait()
            except Exception, e:
                break
            decoded_message = load(message.body.replace('!ruby/sym ', ':'))
            if decoded_message[':requestid'] == self.rid:
                results.append(decoded_message)
        return results
    
    def send_and_await_results(self, timeout=2, debug=False):
        '''Send the prepared RPC message, wait a set period and collect the results.

        :param timeout: Time to wait for a response.
        :type timeout: int
        :param debug: if true, the message will be printed to standard error.
        :type debug: boolean
        :rtype: list of STOMP messages which match this object's `:requestid`'''
        self.subscribe_to_replies()
        self.send(debug=debug)
        sleep(timeout)
        return self.collect_results()
