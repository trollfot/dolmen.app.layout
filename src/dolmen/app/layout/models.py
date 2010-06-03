# -*- coding: utf-8 -*-

import grok
import megrok.layout
import megrok.z3ctable

from dolmen import menu
from dolmen.forms import crud
from dolmen.app.layout import interfaces as API
from dolmen.app.layout import IDisplayView
from dolmen.app.layout import ContextualMenu

from zeam.form import composed
from zope.interface import moduleProvides


class Page(megrok.layout.Page):
    """A dolmen site page.
    """
    grok.baseclass()
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)


class TablePage(megrok.z3ctable.TablePage):
    """A table rendered as a page.
    """
    grok.baseclass()


@menu.menuentry(ContextualMenu)
class Index(Page):
    """A simple index for dolmen objects.
    """
    grok.baseclass()
    grok.name('index')
    grok.title(crud.i18n(u"View"))
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)


@menu.menuentry(ContextualMenu)
class DefaultView(crud.Display):
    """The view per default for dolmen contents.
    """
    grok.name('index')
    grok.implements(IDisplayView)
    grok.require("dolmen.content.View")


class Form(crud.ApplicationForm):
    """A simple dolmen form.
    """
    grok.baseclass()
    grok.require("dolmen.content.View")
    ignoreContext = True


class SubForm(composed.SubForm):
    """A SubForm base class with a nice template.
    """
    grok.baseclass()


class Add(crud.Add):
    """A generic form to add contents.
    """
    pass


@menu.menuentry(ContextualMenu)
class Edit(crud.Edit):
    """A generic form to edit contents.
    """
    grok.require("dolmen.content.Edit")


@menu.menuentry(ContextualMenu)
class Delete(crud.Delete):
    """A delete form.
    """
    grok.require("dolmen.content.Delete")

    @property
    def successMessage(self):
        message = crud.Delete.successMessage.fget(self)
        self.flash(message)
        return message

    @property
    def failureMessage(self):
        self.flash(crud.Delete.failureMessage)
        return crud.Delete.failureMessage


moduleProvides(API.IModels, API.IBaseViews)
__all__ = list(API.IModels) + list(API.IBaseViews)
