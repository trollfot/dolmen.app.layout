# -*- coding: utf-8 -*-

import dolmen.view
import dolmen.menu
import grokcore.security as grok

from cromlech.browser import IHTTPRequest
from cromlech.webob.response import Response
from dolmen.app.layout import get_template
from dolmen.app.layout import interfaces as API, IDisplayView, ContextualMenu
from dolmen.app.security import permissions
from dolmen.forms import crud, base

from zope.interface import implements, moduleProvides


class Page(dolmen.view.View):
    """A dolmen site page.
    """
    grok.baseclass()
    dolmen.view.request(IHTTPRequest)
    grok.require(permissions.CanViewContent)

    implements(IDisplayView)

    responseFactory = Response
    make_response = dolmen.view.make_layout_response


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
    template = get_template('display.pt')
    make_response = dolmen.view.make_layout_response


class Form(base.Form):
    """A base dolmen form.
    """
    grok.baseclass()
    grok.require(permissions.CanViewContent)

    ignoreContext = True
    responseFactory = Response
    template = get_template('form.pt')
    make_response = dolmen.view.make_layout_response


class Add(crud.Add):
    """A generic form to edit contents.
    """
    grok.name('add')
    grok.require(permissions.CanAddContent)

    responseFactory = Response
    template = get_template('form.pt')
    make_response = dolmen.view.make_layout_response


@dolmen.menu.menuentry(ContextualMenu, order=20)
class Edit(crud.Edit):
    """A generic form to edit contents.
    """
    grok.name('edit')
    grok.require(permissions.CanEditContent)

    responseFactory = Response
    template = get_template('form.pt')
    make_response = dolmen.view.make_layout_response


@dolmen.menu.menuentry(ContextualMenu, order=30)
class Delete(crud.Delete):
    """A delete form.
    """
    grok.name('delete')
    grok.require(permissions.CanDeleteContent)

    responseFactory = Response
    template = get_template('form.pt')
    make_response = dolmen.view.make_layout_response


moduleProvides(API.IModels, API.IBaseViews)
__all__ = list(API.IModels) + list(API.IBaseViews)
