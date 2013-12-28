from . import base


class TestWithStompMCo22x(base.MCollective20x, base.IntegrationTestCase):
    '''MCollective integration test case.'''
    CTXT = {
        'connector': 'stomp',
        'plugin.stomp.host': 'localhost',
        'plugin.stomp.port': '61614',
        'plugin.stomp.user': 'mcollective',
        'plugin.stomp.password': 'marionette',
        'topicprefix': 'topic',
    }
