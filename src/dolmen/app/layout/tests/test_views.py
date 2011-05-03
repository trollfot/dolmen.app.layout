# -*- coding: utf-8 -*-

from cromlech.io.testing import TestRequest
from dolmen.app.layout import models
from dolmen.forms.crud import IFactoryAdding
from zope.location import Location
from zope.interface import implements
from zope.testing.cleanup import cleanUp
from zope.component import getMultiAdapter
from dolmen.forms.base import testing


class Folder(Location, dict):
    pass


class Adding(Location):
    implements(IFactoryAdding)
  
    def __init__(self, context, request, factory):
        self.context = context
        self.request = request
        self.factory = factory
        self.__parent__ = context
 
    def add(self, obj):
        id = str(len(self.context) + 1)
        self.context[id] = obj
        obj.__name__ = id
        obj.__parent__ = self.context
        return obj


def setup_module(module):
    testing.grok("dolmen.app.layout")


def teardown_module(module):
    cleanUp()


def test_registered_models():
    folder = Folder()
    request = TestRequest()

    view = getMultiAdapter((folder, request), name="index")
    assert view.__class__ == models.DefaultView

    edit = getMultiAdapter((folder, request), name="edit")
    assert edit.__class__ == models.Edit

    adder = Adding(folder, request, object)
    add = getMultiAdapter((adder, request), name="add")
    assert add.__class__ == models.Add

    delete = getMultiAdapter((folder, request), name="delete")
    assert delete.__class__ == models.Delete
