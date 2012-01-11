# -*- coding: utf-8 -*-

from dolmen.layout import Layout
from dolmen.viewlet import ViewletManager
from dolmen.resources import ResourcesManager
from dolmen.app.layout import interfaces as API, get_template

from cromlech.io import request
from cromlech.browser import IHTTPRequest
from cromlech.webob.response import Response
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
    responseFactory = Response

    def render(self, *args, **kwargs):
        view = self.push_in.get('view')
        if view is not None:
            resources = Resources(self.context, self.request, view)
            resources()
        return Layout.render(self, *args, **kwargs)


moduleProvides(API.IGlobalUI)
__all__ = list(API.IGlobalUI)
