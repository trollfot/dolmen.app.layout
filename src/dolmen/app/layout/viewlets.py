# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
from dolmen.app.layout import master
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from zope.i18nmessageid import MessageFactory
from z3c.flashmessage.interfaces import IMessageReceiver

_ = MessageFactory("dolmen.app.layout")


class Breadcrumbs(grok.Viewlet):
    grok.context(Interface)
    grok.name('dolmen.breadcrumbs')
    grok.viewletmanager(master.DolmenTop)
    grok.order(30)

    def update(self):
        self.crumbs = getMultiAdapter((self.context, self.request),
                                      name="absolute_url").breadcrumbs()


class FlashMessages(grok.Viewlet):
    grok.context(Interface)
    grok.name('dolmen.messages')
    grok.viewletmanager(master.DolmenAboveBody)
    
    def update(self):
        source = getUtility(IMessageReceiver)
        self.messages = list(source.receive())


class Search(grok.Viewlet):
    grok.context(Interface)
    grok.name('dolmen.search')
    grok.viewletmanager(master.DolmenTop)
    grok.order(10)

    def update(self):
        self.term = self.request.form.get('search_term', u'')
