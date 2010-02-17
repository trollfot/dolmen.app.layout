# -*- coding: utf-8 -*-

import grok
from dolmen.app.layout import Page
from zope.publisher.interfaces import INotFound
from zope.location import LocationProxy
from zope.site.hooks import getSite

grok.templatedir("templates")


class NotFound(Page):
    grok.name("index.html")
    grok.context(INotFound)
    grok.require("zope.Public")

    @apply
    def context():
        """This is done to avoid redefining context in the __init__, after
        calling Page.__init__. This way, the located error is the one and
        only context.
        """
        def fset(self, error):
            self._context = LocationProxy(error, error.ob, "Not found")
        def fget(self):
            return self._context
        return property(fget, fset)
        
    def update(self):
        self.request.response.setStatus(404)
