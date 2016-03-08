# -*- coding: utf-8 -*-
"""`pyjector.pyjector` module.

Provides the main dependency-injection class implementation.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '2015-3-28'
__version__ = '0.0.1'
__all__ = ['InjectionError', 'Injector']

import functools
import inspect


class InjectionError(Exception):
    """Base Exception class.
    """
    pass


class Injector(object):
    """Main Injection class that can help implement DP pattern.

    `pyjector.Injector` class is a helper class for implementing the well-known
    `Dependency-Injection` pattern. Provides a user-friendly decorator API for
    injecting callables (functions or classes) into any function/class/methods
    you want.

    Features:
        - Register callables with aliases in injector (decorated, or method).
        - Dict-like access in registered callables.
        - Partial Wrap callables registered in injector instances..
        - Doesn't affect callables that don't require specific dependency.

    Examples:

            >>> injector = Injector()
            >>>
            >>> @injector.provider('days')
            ... def days_function():
            ...     return 365
            ...
            >>> @injector.inject('days')
            ... def days_handler(days, year=1):
            ...     return days(), year
            ...
            >>> print days_handler(year=3)
            (365, 3)

    .. note :: Using the decorator syntax or not, you must be ware of the
    relative path imports in your code. In the docs tutorial we describe a
    proper way of creating dependencies in a modular way, that your api can
    be tested independently from other parts of code.

    """

    __slots__ = ('__mapper')

    version = tuple(map(int, __version__.split('.')))

    def __init__(self):
        self.__mapper = {}

    @property
    def api(self):
        """Returns Injector instance registered callables aliases.
        """
        return self.__mapper.keys()

    def register_callable(self, callable_obj, keyword=None, **init_kwargs):
        """Register new Injection object in injector instance.

        Args:
            callable_obj (object): Callable object (function or class)
            keyword (str): The callable `alias` in injector instance.
            **init_kwargs (dict): Params wrapped in callable.

        Returns:
             Self Injection instance (in order to be used on cascade).

        Raises:
            InjectionError, if `keyword` already registered in injector.

        Examples:
            >>> injector = Injector()
            >>> fn = lambda x, y, z: x+y+z
            >>> injector.register_callable(fn, 'my_fn', x=1, y=1, z=3)
            >>> print injector['my_fn']()
            5
        """
        if keyword in self.api:
            raise InjectionError("`{}` keyword already exists"
                                 .format(keyword))
        if init_kwargs:
            callable_obj = functools.partial(callable_obj, **init_kwargs)

        self[keyword] = callable_obj

    def provider(self, keyword=None, **init_kwargs):
        """Implements the same functionality as `Injector.register_callable`
        as decorator.


        Args:
            keyword (str): The callable `alias` in injector instance.
            init_kwargs (dict): Params wrapped in callable

        Keyword Args:
            init_kwargs (dict): Params wrapped in callable

        Raises:
            InjectionError: If `keyword` already registered in injector.

        Examples:

            >>> injector = Injector()
            >>> @injector.provider('something', async=True)
            ... def some_callable(async=False):
            ...     return async
            ...
            >>> injector['something']()
            True
        """
        def _wrapped(callable_obj):
            self.register_callable(callable_obj, keyword, **init_kwargs)

        return _wrapped

    def inject(self, *keyword):
        """Inject a dependency based on alias. The implementation is
        decorator-based.

            The main idea is that our injector instance only injects the
        requested object only if decorated function accepts an argument with
        the same name as the alias of the callable. If this doesn't happen,
        the `Injector.inject` methods returns the decorated function as is.

        Args:
            keyword (list): The callable `alias` in injector instance.

        Returns:
            The decorated callable instance

        Raises:
            InjectionError if keyword not found in instance `api` property.

        Examples:

            >>> injector = Injector()
            >>>
            >>> @injector.provider('days')
            ... def days_function():
            ...     return 365
            ...
            >>> @injector.inject('days')
            ... def days_handler(days, year=1):
            ...     return days(), year
            ...
            >>> days_handler(year=3)
            (365, 3)
        """
        kw_set = set(keyword)
        api_set = set(self.api)


        def _wrapped(callable_obj):

            @functools.wraps(callable_obj)
            def __wrapped(*args, **kwargs):

                callable_set = set(inspect.getargspec(callable_obj).args)

                inject_set = kw_set.intersection(api_set) if kw_set else api_set

                for kw in inject_set.intersection(callable_set):
                    kwargs[kw] = self[kw]

                return callable_obj(*args, **kwargs)

            return __wrapped

        return _wrapped

    def __str__(self):
        return '<Injector> instance: ({})'.format(
            ', '.join(self.api)
        )

    def __repr__(self):  # pragma: no cover
        return "<{} instance at: 0x{:x}>".format(
            self.__class__.__name__,
            id(self)
        )

    def __iter__(self):  # pragma: no cover
        for keyword in self.api:
            yield keyword

    def __setitem__(self, key, value):
        self.__mapper[key] = value

    def __getitem__(self, key):
        return self.__mapper[key]

    def __delitem__(self, key):
        del self.__mapper[key]

    def __contains__(self, item):
        return item in list(self.__mapper.keys()) + list(self.__mapper.values())
