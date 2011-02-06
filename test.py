#!/usr/bin/python
from mcollective import Message
from yaml import load
from M2Crypto.RSA import load_pub_key, load_key
from stompy.simple import Client
from sys import argv, exit, stderr

if len(argv) < 7:
    print >>stderr, '%s <stomp server> <stomp username> <stomp password> <key filename> <key name> <fact>' % argv[0]
    exit(-1)

certificate_name = argv[5]
stomp_client = Client(argv[1])
stomp_client.connect(argv[2], argv[3])
private_key = load_key(argv[4])

body = {':caller': 'cert=%s' % certificate_name, ':data': {':process_results': True}, ':action': 'inventory', ':agent': 'rpcutil'}

m = Message(body, stomp_client)
m.sign(private_key, certificate_name)
results = m.send_and_await_results(debug=True)

print [load(q[':body'])[':data'][':facts'][argv[6]] for q in results]
