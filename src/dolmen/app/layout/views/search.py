# -*- coding: utf-8 -*-

import grok
from dolmen.app.layout import Page
from zope.interface import Interface
from zope.component import getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.security.management import checkPermission


class SearchResults(Page):
    grok.context(Interface)
    grok.require("dolmen.content.View")

    template = grok.PageTemplateFile('searchresults.pt')

    def update(self):
        self.results = []
        self.term = self.request.form.get('search_term', u'')
        if not len(self.term) > 1:
            return

        catalog = getUtility(ICatalog)
        self.results = [obj for obj in
                        catalog.searchResults(searchabletext=self.term+'*')
                        if checkPermission("dolmen.content.View", obj)]
