# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `pyjector` package.
"""

__author__ = 'Papavassiliou Vassilis'

import pytest
from pyjector import NonUniqueKeyError

raises = getattr(pytest, 'raises')


def test_inject_callable_registry(injector, callable_obj):
    """Testing callable registry

    Args:
        injector (instance): Injector instance.
        callable_obj (instance): Callable object instance.
    """
    injector.register_callable(
        callable_obj=callable_obj,
        keyword='strategy'
    )

    assert injector['strategy'] is callable_obj


def test_inject_callable_run(injector):
    """
    """
    assert injector['strategy']('foo', 'bar') == '(foo: bar)'


def test_inject_single_keyword_registry(injector):
    """
    """
    with raises(NonUniqueKeyError):
        injector.register_callable(
            callable_obj=lambda: 'FooBar',
            keyword='strategy'
        )
