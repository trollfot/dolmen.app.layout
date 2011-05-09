# -*- coding: utf-8 -*-

import dolmen.view
import dolmen.layout
import dolmen.menu
import dolmen.message
import grokcore.security as grok

from cromlech.io import IRequest
from cromlech.webob.response import Response
from dolmen.app.layout import interfaces as API, IDisplayView, ContextualMenu
from dolmen.app.security import permissions
from dolmen.forms import crud, base
from dolmen.app.layout import utils

from zope.interface import implements, moduleProvides


class Page(dolmen.view.View):
    """A dolmen site page.
    """
    grok.baseclass()
    grok.require(permissions.CanViewContent)

    dolmen.view.request(IRequest)
    implements(IDisplayView)

    layout_name = u""
    responseFactory = Response
    __call__ = utils.layout_view_renderer


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

    responseFactory = Response
    __call__ = utils.layout_form_renderer


class Form(base.Form):
    """A base dolmen form.
    """
    grok.baseclass()
    grok.require(permissions.CanViewContent)

    ignoreContext = True
    responseFactory = Response
    __call__ = utils.layout_form_renderer


class Add(crud.Add):
    """A generic form to edit contents.
    """
    grok.name('add')
    grok.require(permissions.CanAddContent)

    responseFactory = Response
    __call__ = utils.layout_form_renderer


@dolmen.menu.menuentry(ContextualMenu, order=20)
class Edit(crud.Edit):
    """A generic form to edit contents.
    """
    grok.name('edit')
    grok.require(permissions.CanEditContent)

    responseFactory = Response
    __call__ = utils.layout_form_renderer


@dolmen.menu.menuentry(ContextualMenu, order=30)
class Delete(crud.Delete):
    """A delete form.
    """
    grok.name('delete')
    grok.require(permissions.CanDeleteContent)

    responseFactory = Response
    __call__ = utils.layout_form_renderer


moduleProvides(API.IModels, API.IBaseViews)
__all__ = list(API.IModels) + list(API.IBaseViews)
