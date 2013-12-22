# coding: utf-8
import logging

from pymco import config
from pymco import rpc
from pymco import message

logging.basicConfig()

config = config.Config.from_configfile('server.cfg')
msg = message.Message(body='ping', agent='discovery', config=config)
action = rpc.SimpleAction(config=config, msg=msg, agent='discovery')
print action.call()
