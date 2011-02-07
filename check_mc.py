#!/usr/bin/python
from mcollective import Message
from yaml import load, dump
from M2Crypto.RSA import load_pub_key, load_key
from stompy.simple import Client
from sys import argv, exit, stderr
from math import floor

if len(argv) < 6:
    print >>stderr, '%s <stomp server> <stomp username> <stomp password> <key filename> <key name> <command> <args>' % argv[0]
    exit(-1)

certificate_name = argv[5]
stomp_client = Client(argv[1])
stomp_client.connect(argv[2], argv[3])
private_key = load_key(argv[4])

body = {':caller': 'cert=%s' % certificate_name, ':data': {':process_results':
True, ':args': argv[7], ':plugin': argv[6]}, ':action':
'runcommand', ':agent': 'icinga'}

m = Message(body, stomp_client, target='icinga')
m.sign(private_key, certificate_name)
results = m.send_and_await_results()

data = [load(q[':body'])[':data'] for q in results]

our_output = " - ".join([o[':output'] for o in data])
exit_codes = [o[':exitcode'] for o in data]

try:
    our_exit_code = int(floor(sum(exit_codes, 0.0) / len(exit_codes)))
except ZeroDivisionError:
    our_exit_code = 3

print our_output
exit(our_exit_code)
