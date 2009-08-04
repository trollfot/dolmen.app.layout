# -*- coding: utf-8 -*-

import grok
import master
from megrok.z3cform import Form
from dolmen.content import IContainer
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from zope.dublincore.interfaces import IZopeDublinCore
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.i18nmessageid import MessageFactory
from zope.app.component.hooks import getSite
from z3c.flashmessage.interfaces import IMessageReceiver

_ = MessageFactory("dolmen.app.layout")
grok.context(Interface)


class Breadcrumbs(grok.Viewlet):
    grok.name('dolmen.breadcrumbs')
    grok.viewletmanager(master.DolmenTop)
    grok.order(30)

    def update(self):
        self.crumbs = getMultiAdapter((self.context, self.request),
                                      name="absolute_url").breadcrumbs()


class Authors(grok.Viewlet):
    grok.name('dolmen.authors')
    grok.viewletmanager(master.DolmenFooter)


class ContentInformations(grok.Viewlet):
    grok.name('dolmen.byline')
    grok.context(IAttributeAnnotatable)
    grok.viewletmanager(master.DolmenBelowBody)
    grok.order(20)

    creation = u""
    modification = u""
    
    def update(self):
        dc = IZopeDublinCore(self.context)
        formatter = self.request.locale.dates.getFormatter('dateTime')

        if dc.created:
            self.creation = _(
                u"Created by ${name} the ${date}",
                mapping={'name': dc.creators and dc.creators[0],
                         'date': formatter.format(dc.created)}
                )
        
        if dc.modified:
            self.modification =  _(
                u"Last modified the ${date}",
                mapping={'date': formatter.format(dc.modified)}
                )
 

class FlashMessages(grok.Viewlet):
    grok.name('dolmen.messages')
    grok.viewletmanager(master.DolmenAboveBody)
    
    def update(self):
        source = getUtility(IMessageReceiver)
        self.messages = list(source.receive())


class Search(grok.Viewlet):
    grok.name('dolmen.search')
    grok.viewletmanager(master.DolmenTop)
    grok.order(10)

    def update(self):
        self.term = self.request.form.get('search_term', u'')


class MetaTags(grok.Viewlet):
    grok.order(10)
    grok.name('dolmen.metatags')
    grok.context(IAttributeAnnotatable)
    grok.viewletmanager(master.DolmenHeader)

    def update(self):
        self.root = getSite()
        self.DublinCore = IZopeDublinCore(self.context, None)

    @property
    def title(self):
        if self.DublinCore is not None and self.context is not self.root:
            return "%s &mdash; %s" % (self.DublinCore.title, self.root.title)
        return self.root.title
