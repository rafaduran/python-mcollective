'''Tests for messaging objects.'''
import pytest

from pymco import exc
from pymco import message
from pymco.test import ctxt


@pytest.fixture
def msg_no_filter(config):
    '''Creates a new :py:class:`pymco.message.Message` instance.'''
    return message.Message(body=ctxt.MSG['body'],
                           agent=ctxt.MSG['agent'],
                           config=config)


def test_filter_add_cfclass(filter_):
    '''Tests :py:method:`pymco.message.Filter.add_class`.'''
    assert filter_['cf_class'] == []
    filter_.add_cfclass('common::linux')
    assert filter_['cf_class'] == ['common::linux']
    filter_.add_cfclass('apache')
    assert filter_['cf_class'] == ['common::linux', 'apache']


def test_filter_add_agent(filter_):
    '''Tests :py:method:`pymco.message.Filter.add_agent`.'''
    assert filter_['agent'] == []
    filter_.add_agent('package')
    assert filter_['agent'] == ['package']
    filter_.add_agent('registration')
    assert filter_['agent'] == ['package', 'registration']


def test_filter_add_fact(filter_):
    '''Tests :py:method:`pymco.message.Filter.add_fact` happy path.'''
    assert filter_['fact'] == []
    filter_.add_fact(fact='country', value='/uk/')
    assert filter_['fact'] == [{':fact': "country", ':value': "/uk/"}]
    filter_.add_fact(fact='country', value='/uk/', operator='==')
    assert filter_['fact'] == [
        {':fact': "country", ':value': "/uk/"},
        {':fact': "country", ':value': "/uk/", ':operator': '=='},
    ]


def test_filter_add_fact_operators(filter_):
    '''Tests :py:method:`pymco.message.Filter.add_fact` accepts only
    MCollective supported operators.'''
    for operator in ('==', '<=', '>=', '>', '<', '!='):
        filter_.add_fact(fact='country', value='/uk/', operator=operator)

    with pytest.raises(exc.BadFilterFactOperator):
        filter_.add_fact(fact='country', value='/uk/', operator='bad')


def test_filter_add_identity(filter_):
    '''Tests :py:method:`pymco.message.Filter.add_identity`.'''
    assert filter_['identity'] == []
    filter_.add_identity('foo.bar.com')
    assert filter_['identity'] == ['foo.bar.com']
    filter_.add_identity('spam.bar.com')
    assert filter_['identity'] == ['foo.bar.com', 'spam.bar.com']


def test_filter_method_chaining(filter_):
    '''Tests :py:class:`pymco.message.Filter` method chaining.'''
    assert dict(filter_) == {'cf_class': [],
                             'agent': [],
                             'fact': [],
                             'identity': [],
                             'compound': [],
                             }
    filter_.add_agent('package').add_identity('foo.bar.com')
    assert dict(filter_) == {'cf_class': [],
                             'agent': ['package'],
                             'fact': [],
                             'identity': ['foo.bar.com'],
                             'compound': [],
                             }


def test_filter_length(filter_):
    '''Tests :py:meth:`pymco.message.Filter.__len__`.'''
    assert len(filter_) == 5  # cf_class, agent, fact, identity, compound
    filter_.add_agent('package')
    assert len(filter_) == 5


def test_message(msg, filter_):
    '''Tests :py:class:`pymco.message.Message` attribues.'''
    for name, value in ((':senderid', 'mco1'),
                        (':msgtime', int(ctxt.MSG['msgtime'])),
                        (':ttl', 60),
                        (':requestid', ctxt.MSG['requestid']),
                        (':body', ctxt.MSG['body']),
                        (':agent', ctxt.MSG['agent']),
                        (':collective', 'mcollective'),
                        (':filter', dict(filter_)),
                        ):
        assert msg[name] == value


def test_message_length(msg):
    '''Tests :py:method:`pymco.message.Message.length`.'''
    assert len(msg) == len(msg._message)


def test_message_iteration(msg):
    '''Tests :py:method:`pymco.message.Message.__iter__`.'''
    assert sorted(list(msg)) == sorted(list(msg._message.keys()))


def test_message_raises_improperly_configured(config, filter_):
    '''Tests :py:class:`pymco.message.Message` raises
    :py:exc:`pymco.exc.ImproperlyConfigured` if configuration doesn't contain
    all required information.'''
    with pytest.raises(exc.ImproperlyConfigured):
        message.Message(body='ping',
                        agent='discovery',
                        config={},
                        filter_=dict(filter_))


def test_message_set_item(msg):
    '''Tests :py:meth:`pymco.message.Message.__setitem__`.'''
    msg[':test'] = 123
    assert msg[':test'] == 123


def test_message_del_item(msg):
    '''Tests :py:meth:`pymco.message.Message.__delitem__`.'''
    msg[':test'] = 123
    assert msg[':test'] == 123
    del msg[':test']
    with pytest.raises(KeyError):
        msg[':test']


def test_message_filter_update(msg):
    '''Tests :py:meth:`pymco.message.Message.__setitem__` maintains filter as
    a dict-like object.'''
    filter_ = message.Filter()
    msg[':filter'] = filter_
    assert msg[':filter'] == dict(filter_)
    assert isinstance(msg[':filter'], dict)


def test_message_no_filter(msg_no_filter):
    '''Tests :py:class:`pymco.message.Message` with no filter.'''
    assert dict(msg_no_filter[':filter']) == dict(message.Filter())


def test_msg_update_no_symbol(msg):
    """Test update msg with a non symbol raises ValueError"""
    with pytest.raises(ValueError):
        msg['foo'] = 'foo'
