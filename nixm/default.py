# This file is placed in the Public Domain
# pylint: disable=C,R


"autoconstruct"


from .object import Object


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")
