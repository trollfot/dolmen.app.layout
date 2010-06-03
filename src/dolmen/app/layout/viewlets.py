# -*- coding: utf-8 -*-

import grok

from dolmen.app.layout import interfaces as API
from dolmen.app.layout import ContextualMenu, MenuViewlet, AboveBody, Top

from zope.component import queryUtility
from zope.interface import Interface, moduleProvides
from z3c.flashmessage.interfaces import IMessageReceiver


class FlashMessages(grok.Viewlet):
    grok.order(10)
    grok.context(Interface)
    grok.name('dolmen.messages')
    grok.viewletmanager(AboveBody)

    def update(self):
        source = queryUtility(IMessageReceiver)
        if source is not None:
            self.messages = list(source.receive())
        else:
            self.messages = []


class ContextualActions(MenuViewlet):
    grok.context(Interface)
    grok.viewletmanager(Top)
    grok.order(50)

    menu_factory = ContextualMenu

    def render(self):
        if len(self.menu.viewlets) > 1:
            return self.menu.render()
        return u""


moduleProvides(API.IContextualUI)
__all__ = list(API.IContextualUI)
