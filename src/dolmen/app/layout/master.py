# -*- coding: utf-8 -*-

import os
import grok
from megrok.layout import Layout
from zope.interface import Interface
from grokcore.view import PageTemplateFile

grok.templatedir('templates')


class Master(Layout):
    grok.name('master')
    grok.context(Interface)

    def update(self):
        self.base = str(self.request.URL.get(-1))

        
class DolmenHeader(grok.ViewletManager):
    grok.name("dolmen.header")
    grok.context(Interface)
    

class DolmenTop(grok.ViewletManager):
    grok.name("dolmen.top")
    grok.context(Interface)


class DolmenFooter(grok.ViewletManager):
    grok.name("dolmen.footer")
    grok.context(Interface)


class DolmenBody(grok.ViewletManager):
    grok.name("dolmen.body")
    grok.context(Interface)


class DolmenAboveBody(grok.ViewletManager):
    grok.name("dolmen.above.body")
    grok.context(Interface)


class DolmenBelowBody(grok.ViewletManager):
    grok.name("dolmen.below.body")
    grok.context(Interface)
