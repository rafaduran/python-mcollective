[![Stories in Ready](https://badge.waffle.io/rafaduran/python-mcollective.png?label=ready)](https://waffle.io/rafaduran/python-mcollective)  
mcollective-python
==================

[![Build Status](https://travis-ci.org/rafaduran/python-mcollective.png)](https://travis-ci.org/rafaduran/python-mcollective)
[![Coverage Status](https://coveralls.io/repos/rafaduran/python-mcollective/badge.png?branch=master)](https://coveralls.io/r/rafaduran/python-mcollective?branch=master)
[![codeq](https://codeq.io/github/rafaduran/python-mcollective/badges/master.png)](https://codeq.io/github/rafaduran/python-mcollective/branches/master)

This is an example Python binding for Marionette Collective RPC.

[API Documentation](http://insom.github.com/mcollective-python/)

The main class is `Message`, and you create an instance of this to initiate
some RPC. It takes a dictionary which contains the actual request (following
[the MCollective RPC documentation][rpc]) and a stomp.Client instance for
future use.

You can then .sign() a request, with your private key, .subscribe_to_replies(),
manually .send() and then .collect_results() - or just do a
.send_and_await_results() after signing to receive an array of STOMP messages
back.

[rpc]: http://docs.puppetlabs.com/mcollective/reference/basic/messageformat.html

Requirements
------------

* M2Crypto - seems to be the most comprehensive OpenSSL binding, though I needed
  to read the source.

* stompy - make Python speak STOMP.

And it also requires you to have particular MCollective setup:

	securityprovider = ssl
	plugin.ssl_serializer = yaml

The Quick Start
---------------

	# Run the test client
	$ python test.py localhost username password aaron-private.pem aaron-public uptime

License
-------

Copyright (c) 2011, Aaron Brady, Interactive Web Solutions Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
