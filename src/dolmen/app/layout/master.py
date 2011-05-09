# -*- coding: utf-8 -*-

from dolmen.layout import Layout
from dolmen.viewlet import ViewletManager
from dolmen.template import TALTemplate
from dolmen.container.interfaces import IContainer
from dolmen.location import get_absolute_url
from dolmen.resources import ResourcesManager

from dolmen.app.layout import interfaces as API
from dolmen.app.layout import utils

from cromlech.webob.response import Response
from grokcore.component import context, name
from zope.interface import Interface, moduleProvides


class Resources(ResourcesManager):
    name('dolmen.resources')
    context(Interface)


class Header(ViewletManager):
    name("dolmen.header")
    context(Interface)


class Top(ViewletManager):
    name("dolmen.top")
    context(Interface)


class Footer(ViewletManager):
    name("dolmen.footer")
    context(Interface)


class AboveBody(ViewletManager):
    name("dolmen.above.body")
    context(Interface)


class BelowBody(ViewletManager):
    name("dolmen.below.body")
    context(Interface)


class Master(Layout):
    context(Interface)

    template = TALTemplate(utils.template_path('master.pt'))
    responseFactory = Response

    def update(self, *args, **extra):
        Layout.update(self, *args, **extra)
        if 'view' in self.push_in:
            resources = Resources(
                self.context, self.request, self.push_in['view'])
            resources()


moduleProvides(API.IGlobalUI)
__all__ = list(API.IGlobalUI)
