# -*- coding: utf-8 -*-

import megrok.menu
import grokcore.viewlet

from zope.component import getUtility
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.publisher.interfaces.browser import IBrowserMenu


class ContextualMenu(megrok.menu.Menu):
    megrok.menu.name('contextual')
    megrok.menu.title('Contextual actions')


class DisplayMenu(megrok.menu.Menu):
    megrok.menu.name('display')
    megrok.menu.title('Content display')
    

class MenuViewlet(grokcore.viewlet.Viewlet):
    grokcore.viewlet.baseclass()
    grokcore.viewlet.require("dolmen.content.View")

    template = grokcore.viewlet.PageTemplateFile("templates/genericmenu.pt")
    
    entry_class = ""
    actions = []

    @property
    def menu_name(self):
        raise NotImplementError("You need to specify a menu name.")

    def get_context(self):
        return self.context

    def get_actions(self, context):
        menu = getUtility(IBrowserMenu, self.menu_name)
        actions = menu.getMenuItems(context, self.request)
        return menu.title, actions

    def update(self):
        """Gets the actions and determines which is the selected one.
        """
        context = self.get_context()
        self.title, actions = self.get_actions(context)
        
        if actions:
            url = absoluteURL(context, self.request)
            selected = getattr(self.view, '__name__', None)
            self.actions = [{'url': "%s/%s" % (url, action['action']),
                             'title': action['title'],
                             'css': (action['action'] == selected
                                     and self.entry_class + ' selected'
                                     or self.entry_class)}
                            for action in actions]
