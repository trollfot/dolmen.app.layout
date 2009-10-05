# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
import dolmen.content
from dolmen.app.layout import master, MenuViewlet
from zope.interface import Interface
from zope.component import getUtility
from z3c.flashmessage.interfaces import IMessageReceiver


class FlashMessages(grok.Viewlet):
    grok.order(10)
    grok.context(Interface)
    grok.name('dolmen.messages')
    grok.viewletmanager(master.DolmenAboveBody)
    
    def update(self):
        source = getUtility(IMessageReceiver)
        self.messages = list(source.receive())


class ContextualActions(MenuViewlet):
    grok.context(dolmen.content.IBaseContent)
    grok.viewletmanager(master.DolmenTop)
    grok.order(50)

    menu_name = u'contextual'

    def get_actions(self, context):
        actions = MenuViewlet.get_actions(self, context)
        if len(actions) <= 1:
            return []
        return actions
