# -*- coding: utf-8 -*-

import dolmen.view
import dolmen.layout
import dolmen.menu
import grokcore.security as grok

from cromlech.io import IRequest
from dolmen.app.layout import interfaces as API, IDisplayView, ContextualMenu
from dolmen.app.security import content as permissions
from dolmen.forms import crud
from dolmen.message import utils

from zope.interface import implements, moduleProvides


class Page(dolmen.view.View):
    """A dolmen site page.
    """    
    grok.baseclass()
    grok.require(permissions.CanViewContent)

    dolmen.view.request(IRequest)
    implements(IDisplayView)

    layout_name = u""

    def __call__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        if not self.response.status_int in [301, 302]:
            layout = dolmen.layout.query_layout(
                self.request, self.context,
                dolmen.layout.ILayout, name=self.layout_name)
            return layout(self.render(*args, **kwargs), view=self)
        return self.response


class Index(Page):
    """A simple index for dolmen objects.
    """
    grok.baseclass()
    grok.require(permissions.CanViewContent)
    
    dolmen.view.name('index')
    dolmen.view.title(crud.i18n(u"View"))
    implements(IDisplayView)


@dolmen.menu.menuentry(ContextualMenu, order=10)
class DefaultView(crud.Display):
    """The view per default for dolmen contents.
    """
    dolmen.view.name('index')
    implements(IDisplayView)
    grok.require(permissions.CanViewContent)


class Form(crud.ApplicationForm):
    """A simple dolmen form.
    """
    grok.baseclass()
    grok.require(permissions.CanViewContent)

    ignoreContext = True


class Add(crud.Add):
    """A generic form to edit contents.
    """
    dolmen.view.name('dolmen.add')
    grok.require(permissions.CanAddContent)


@dolmen.menu.menuentry(ContextualMenu, order=20)
class Edit(crud.Edit):
    """A generic form to edit contents.
    """
    grok.require(permissions.CanEditContent)
 

@dolmen.menu.menuentry(ContextualMenu, order=30)
class Delete(crud.Delete):
    """A delete form.
    """
    grok.require(permissions.CanDeleteContent)

    @property
    def successMessage(self):
        message = crud.Delete.successMessage.fget(self)
        utils.send(message)
        return message

    @property
    def failureMessage(self):
        utils.send(crud.Delete.failureMessage)
        return crud.Delete.failureMessage


moduleProvides(API.IModels, API.IBaseViews)
__all__ = list(API.IModels) + list(API.IBaseViews)
