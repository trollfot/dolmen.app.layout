# -*- coding: utf-8 -*-

import grok

from dolmen import menu
from dolmen.app.layout import interfaces as API
from megrok.pagetemplate import PageTemplate

from zope.component import getUtility
from zope.interface import moduleProvides, Interface
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.browsermenu.interfaces import IBrowserMenu


class ContextualMenu(menu.Menu):
    grok.name('contextual-actions')
    grok.context(Interface)
    grok.title('Contextual actions')


class MenuViewlet(grok.Viewlet):
    grok.baseclass()
    grok.require("dolmen.content.View")

    menu_class = u"menu"
    entry_class = u"entry"
    actions = []

    @property
    def menu_factory(self):
        raise NotImplementedError("You need to specify a menu class.")

    def get_context(self):
        return self.context

    def update(self):
        context = self.get_context()
        self.menu = self.menu_factory(context, self.request, self.view)
        self.menu.update()

    def render(self):
        return self.menu.render()
        

moduleProvides(API.IMenus)
__all__ = list(API.IMenus)
