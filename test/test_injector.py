# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `pyjector` package.
"""

__author__ = 'Papavassiliou Vassilis'

import pytest
from pyjector import InjectionError


def test_injector_register_callable(injector, callable_obj):
    """Testing `pyjector.Injector.register_callable` method.
    """
    injector.register_callable(
        callable_obj=callable_obj,
        keyword='op'
    )

    assert injector['op'] is callable_obj


def test_injector_register_callable_error(injector):
    """Testing `pyjector.Injector.register_callable` method error handling on
    duplicate keywords.
    """
    with pytest.raises(InjectionError):
        injector.register_callable(
            callable_obj=lambda: 'FooBar',
            keyword='op'
        )


def test_injector_provider_method(injector):
    """Testing `pyjector.Injector.provider` method.
    """

    injector.provider('add')(lambda x, y: x + y)

    assert injector['add'](1, 100) == 101


def test_injector_provider_method_error(injector):
    """Testing `pyjector.Injector.provider` method error handling on
    duplicate keywords.
    """
    with pytest.raises(InjectionError):
        injector.provider('add')(lambda x, y: x - y)


def test_injector_inject_method_single(injector, custom_func):
    """Testing `pyjector.Injector.inject` method on providing single object.
    """
    custom_fn = injector.inject('op')(custom_func)

    assert custom_fn('foo', 'bar') == '(foo: bar)'


def test_injector_inject_method_multiple(injector):
    """Testing `pyjector.Injector.inject` method on providing single object.
    """

    def test_fn(op, add, x, y):
        return op(add(x, y), add(x + 1, y + 1))

    custom_f = injector.inject('op', 'add')(test_fn)

    assert custom_f(x=1, y=1) == '(2: 4)'


def test_injector_inject_method_invalid_key_error(injector):
    """Testing `pyjector.Injector.inject` method error handling
        on invalid key to provide.
    """
    with pytest.raises(InjectionError):
        return injector.inject('that')(lambda that: that * 2)


def test_injector_inject_method_invalid_callable_parameter_pass(injector):
    """Testing `pyjector.Injector.inject` method error handling
        on providing a callable to function that doesn't accept it.
    """
    test_func = injector.inject('add')(lambda: 'hi')

    assert test_func() == 'hi'


def test_injector_api_property(injector):
    """Testing `pyjector.Injector.api` property.
    """

    assert sorted(injector.api) == sorted(['op', 'add'])


def test_injector_getitem(injector):
    """Testing `pyjector.Injector.__getitem__` method.
    """
    assert injector['op']('foo', 'bar') == '(foo: bar)'


def test_injector_delitem(injector):
    """Testing `pyjector.Injector.__delitem__` method.
    """

    del injector['add']

    assert injector.api == ['op']


def test_injector_setitem(injector):
    """Testing `pyjector.Injector.__setitem__` method.
    """
    injector['art'] = lambda: 'Hi!'

    assert 'art' in injector


def test_injector_contains(injector, callable_obj):
    """Testing `pyjector.Injector.__contains__` method.
    """
    assert callable_obj in injector


def test_injector_str(injector):
    """Testing `pyjector.Injector.__str__` method.
    """
    assert str(injector) == '<Injector> instance: (art, op)'
