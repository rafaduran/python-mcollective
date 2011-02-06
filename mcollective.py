from yaml import load, dump
from time import time, sleep
from hashlib import sha1

class AlreadySentException(Exception):
    pass

class Message:
    def __init__(self, body, stomp_client, prefix='mcollective', target='rpcutil'):
        self.stomp_client = stomp_client
        self.target = '/topic/%s.%s.command' % (prefix, target)
        self.target_reply = '/topic/%s.%s.reply' % (prefix, target)
        self.rid = sha1(str(time())).hexdigest()
        self.sent = False
        r = dict()
        r[':msgtime'] = int(time())
        r[':filter'] = {
            'identity': [],
            'fact': [],
            'agent': [],
            'cf_class': [],
        }
        r[":requestid"] = self.rid
        r[":msgtarget"] = self.target
        r[':body'] = dump(body, explicit_start=True, explicit_end=False)
        self.request = r
    
    def subscribe_to_replies(self):
        self.stomp_client.subscribe(self.target_reply)
    
    def sign(self, private_key, certificate_name, sender_id='python'):
        self.request[":callerid"] = 'cert=%s' % certificate_name
        self.request[":senderid"] = sender_id
        hashed_signature = private_key.sign(sha1(self.request[':body']).digest(), 'sha1')
        self.request[':hash'] = hashed_signature.encode('base64').replace("\n", "").strip()

    def send(self, debug=False):
        if self.sent:
            raise AlreadySentException()
        data = dump(self.request, explicit_start=True, explicit_end=False)
        if debug:
            import sys
            print >>sys.stderr, data
        self.stomp_client.put(data, self.target)
        self.sent = True
    
    def collect_results(self):
        results = []
        while True:
            message = None
            try:
                message = self.stomp_client.get_nowait()
            except Exception, e:
                break
            decoded_message = load(message.body)
            if decoded_message[':requestid'] == self.rid:
                results.append(decoded_message)
        return results
    
    def send_and_await_results(self, timeout=2, debug=False):
        self.subscribe_to_replies()
        self.send(debug=debug)
        sleep(timeout)
        return self.collect_results()
