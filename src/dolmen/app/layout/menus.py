# -*- coding: utf-8 -*-

import dolmen.menu as menu
from dolmen.app.layout import interfaces as API
from dolmen.viewlet import Viewlet
from grokcore.component import baseclass
from grokcore.security import require
from zope.interface import moduleProvides, Interface


class ContextualMenu(menu.Menu):
    menu.context(Interface)
    menu.name('contextual-actions')
    menu.title(u'Contextual actions')


class MenuViewlet(Viewlet):
    baseclass()

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
