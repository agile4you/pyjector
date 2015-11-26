# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `pyjector` package.
"""

__author__ = 'Papavassiliou Vassilis'


import pytest
from pyjector import Injector


@pytest.fixture(scope='session')
def callable_obj():
    """A 'pytest.fixture' that mocks a callable object.
    """

    def _mock_callable(param_1, param_2):
        return "({}: {})".format(param_1, param_2)

    return _mock_callable


@pytest.fixture(scope='session')
def injector():
    """ A'pytest.fixture' that mocks `pyjector.Injector` class instance.
    """

    inst = Injector()

    return inst


@pytest.fixture(scope='session')
def custom_func():
    """A 'pytest.fixture' that mocks a custom function.
    """

    def _custom_function(text_1, text_2, op):
        """A simple custom function that uses an external dependency.

        Args:
            text_1 (str):
            text_2 (str):
            op (callable):

        Returns:
            The result of: op(text_1, text_2)
        """

        return op(text_1, text_2)

    return _custom_function
