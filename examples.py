# -*- coding: utf-8 -*-
"""Example `pyjector` package usage.
"""

from pyjector import Injector

provider = Injector()

fixtures = {chr(i): i for i in range(97, 120)}


class DB(object):
    """A fake db class
    """

    def __init__(self, **fixture):
        self.__data = fixture

    def retrieve(self, pk):
        return self.__data.get(pk)


print(fixtures)

provider.register_callable(DB(**fixtures), 'db')


@provider.inject()
def char_to_integer(db, ch):
    num = db.retrieve(ch)
    return num


print(char_to_integer(ch='c'))
