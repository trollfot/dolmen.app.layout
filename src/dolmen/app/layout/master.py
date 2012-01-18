# -*- coding: utf-8 -*-

from cromlech.browser import IHTTPRequest
from cromlech.io import request
from dolmen.app.layout import interfaces as API, get_template
from dolmen.layout import Layout
from dolmen.resources import ResourcesManager
from dolmen.viewlet import ViewletManager
from grokcore.component import context
from zope.interface import Interface, moduleProvides


class Resources(ResourcesManager):
    context(Interface)
    request(IHTTPRequest)


class Header(ViewletManager):
    context(Interface)
    request(IHTTPRequest)


class Top(ViewletManager):
    context(Interface)
    request(IHTTPRequest)


class Footer(ViewletManager):
    context(Interface)
    request(IHTTPRequest)


class AboveBody(ViewletManager):
    context(Interface)
    request(IHTTPRequest)


class BelowBody(ViewletManager):
    context(Interface)
    request(IHTTPRequest)


class Master(Layout):
    context(Interface)
    request(IHTTPRequest)

    template = get_template('master.pt')

    def render(self, view=None, *args, **kwargs):
        if view is not None:
            resources = Resources(self.context, self.request, view)
            resources()
        return Layout.render(self, view=view, *args, **kwargs)


moduleProvides(API.IGlobalUI)
__all__ = list(API.IGlobalUI)
