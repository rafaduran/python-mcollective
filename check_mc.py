#!/usr/bin/python
from mcollective import Message, Filter
from yaml import load, dump
from M2Crypto.RSA import load_pub_key, load_key
from stompy.simple import Client
from sys import argv, exit, stderr
import os.path
from math import floor

config = {}
for line in file('/etc/mcollective/client.cfg', 'rt').readlines():
    bits = line.split('=', 1)
    if len(bits) == 2:
        config[bits[0].strip()] = bits[1].strip()

if len(argv) < 2:
    print >>stderr, '%s <check> [args]' % argv[0]
    exit(-1)

certificate_name = os.path.basename(config['plugin.ssl_client_public'].replace('.pem', ''))
stomp_client = Client(config.get('plugin.stomp.host', 'localhost'), port=int(config.get('plugin.stomp.port', 61613)))
stomp_client.connect(config['plugin.stomp.user'], config['plugin.stomp.password'])
private_key = load_key(config['plugin.ssl_client_private'])

args = ' '.join(argv[2:])

body = {
    ':caller': 'cert=%s' % certificate_name, 
    ':data': {
        ':process_results': True, 
        ':command': argv[2],
    }, 
    ':action': 'runcommand', 
    ':agent': 'nrpe'
}

m = Message(body, stomp_client, target='nrpe', filter_=Filter(identity=argv[1]).dump())
m.sign(private_key, certificate_name)
results = m.send_and_await_results(timeout=1)
data = [load(q[':body'])[':data'] for q in results]
if len(data):
    print data[0][':output']
    exit(int(data[0][':exitcode']))
print 'No response from MCollective'
exit(3)
