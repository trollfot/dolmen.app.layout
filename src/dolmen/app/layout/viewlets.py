# -*- coding: utf-8 -*-

import dolmen.viewlet
from grokcore.component import baseclass
from zope.interface import Interface, moduleProvides
from dolmen.template import TALTemplate
from dolmen.resources import ResourceViewlet
from dolmen.app.layout import Resources
from dolmen.app.layout import utils, interfaces as API
from dolmen.app.layout import ContextualMenu, MenuViewlet, AboveBody, Top


class Resource(ResourceViewlet):
    baseclass()
    dolmen.viewlet.slot(Resources)


class FlashMessages(dolmen.viewlet.Viewlet):
    dolmen.viewlet.order(10)
    dolmen.viewlet.context(Interface)
    dolmen.viewlet.name('dolmen.messages')
    dolmen.viewlet.slot(AboveBody)

    def update(self):
        received = receive()
        if received is not None:
            self.messages = list(received)
        else:
            self.messages = []


class ContextualActions(MenuViewlet):
    dolmen.viewlet.context(Interface)
    dolmen.viewlet.slot(Top)
    dolmen.viewlet.order(50)

    menu_factory = ContextualMenu
    template = TALTemplate(utils.template_path('menu.pt'))

    def compute_actions(self, viewlets):
        for action in viewlets:
            selected = action.__name__ == self.view.__view_name__            
            yield {
                'id': action.__name__,
                'url': not selected and action.url or None,
                'title': action.title,
                'selected': selected,
                'class': (selected and 'selected ' +
                          self.menu.entry_class or self.menu.entry_class),
                }

    def update(self):
        MenuViewlet.update(self)
        if len(self.menu.viewlets) > 1:
            self.actions = self.compute_actions(self.menu.viewlets)
        else:
            self.actions = None

    def render(self):
        return self.template.render(self)


moduleProvides(API.IContextualUI)
__all__ = list(API.IContextualUI)
