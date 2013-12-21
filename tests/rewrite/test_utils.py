"""Tests for pymco.utils"""
import collections

import mock
import pytest

from pymco import utils


def test_import_class():
    assert utils.import_class('collections.defaultdict') is collections.defaultdict


def test_import_path__raises_import_error__missing_module():
    with pytest.raises(ImportError):
        utils.import_class('foo.spam')


def test_import_path__raises_import_error__missing_class():
    with pytest.raises(ImportError):
        utils.import_class('collections.spam')


def test_import_path_raises_import_error_bad_string():
    with pytest.raises(ImportError):
        utils.import_class('foo')


@mock.patch.object(utils, 'import_class')
def test_import_object_delegates_to_import_class(import_class):
    assert utils.import_object('foo.spam') == import_class.return_value.return_value
    import_class.assert_called_once_with('foo.spam')


@mock.patch.object(utils, 'import_class')
def test_import_object_instantiate_with_the_right_arguments(import_class):
    utils.import_object('foo.spam', 1, foo='spam')
    import_class.return_value.assert_called_once_with(1, foo='spam')
