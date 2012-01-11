# -*- coding: utf-8 -*-

from dolmen.viewlet import testing
from cromlech.browser.testing import TestView, TestHTTPRequest
from zope.testing.cleanup import cleanUp

from dolmen.app.layout import models
from zope.location import Location
from cromlech.browser import IViewSlot

from zope.interface import implements
from zope.component import getAdapters


def setup_module(module):
    testing.grok("dolmen.app.layout.master")


def teardown_module(module):
    cleanUp()


def test_registered_managers():

    context = Location()
    request = TestHTTPRequest()
    
    view = TestView(context, request)
    managers = list(getAdapters((context, request, view), IViewSlot))

    assert len(managers) == 6
    assert set(dict(managers).keys()) == set([
        'abovebody',
        'belowbody',
        'footer',
        'header',
        'resources',
        'top',
        ])
