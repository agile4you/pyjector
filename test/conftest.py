# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `pyjector` package.
"""

__author__ = 'Papavassiliou Vassilis'


import pytest


fixture = getattr(pytest, 'fixture', None)


@fixture(scope='session')
def mock_callable():
    """A 'pytest.fixture' that mocks a callable object.
    """

    def _mock_callable(param_1, param_2):
        return "({}: {})".format(param_1, param_2)

    return _mock_callable
