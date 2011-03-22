#!/usr/bin/python
from mcollective import Message
from yaml import load, dump
from M2Crypto.RSA import load_pub_key, load_key
from stompy.simple import Client
from sys import argv, exit, stderr
from math import floor

config = {}
execfile('/etc/check_mc.rc', config)

if len(argv) < 2:
    print >>stderr, '%s <check> [args]' % argv[0]
    exit(-1)

certificate_name = config['certificate_name']
stomp_client = Client(config.get('host', 'localhost'), port=config.get('port', 61613))
stomp_client.connect(config['username'], config['password'])
private_key = load_key(config['private_key'])

args = ' '.join(argv[2:])

body = {
    ':caller': 'cert=%s' % certificate_name, 
    ':data': {
        ':process_results': True, 
        ':args': args, 
        ':plugin': argv[1],
    }, 
    ':action': 'runcommand', 
    ':agent': 'icinga'
}

m = Message(body, stomp_client, target='icinga')
m.sign(private_key, certificate_name)
results = m.send_and_await_results(timeout=config.get('timeout', 5))

data = [load(q[':body'])[':data'] for q in results]

our_output = " - ".join([o[':output'] for o in data])
exit_codes = [o[':exitcode'] for o in data]

try:
    our_exit_code = int(floor(sum(exit_codes, 0.0) / len(exit_codes)))
except ZeroDivisionError:
    our_exit_code = 3

print our_output
exit(our_exit_code)
