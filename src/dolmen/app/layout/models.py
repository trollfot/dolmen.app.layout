# -*- coding: utf-8 -*-

import megrok.menu
import megrok.layout
import megrok.z3ctable
import grokcore.viewlet as grok
import dolmen.content as content

from zope.component import getUtility
from zope.i18nmessageid import MessageFactory

from megrok.z3cform import composed
from z3c.flashmessage.interfaces import IMessageSource

from dolmen.forms import crud
from dolmen.app.site import IDolmen
from dolmen.app.layout import IDisplayView
from dolmen.forms.base import PageForm, cancellable

_ = MessageFactory("dolmen")


class ApplicationAwareView(object):
    """A mixin allowing to access the application url 
    """
    def application_url(self, name=None):
        """Return the URL of the nearest Dolmen site.
        """
        obj = self.context
        while obj is not None:
            if IDolmen.providedBy(obj):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueError("No application found.")


    def flash(self, message, type='message'):
        """Send a short message to the user.
        """
        source = getUtility(IMessageSource, name='session')
        source.send(message, type)


class Page(megrok.layout.Page, ApplicationAwareView):
    """A dolmen site page.
    """
    grok.baseclass()
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)

    
class TabView(object):
    """A contextual tab.
    """
    grok.baseclass()
    megrok.menu.menuitem('contextual-actions')


class TablePage(megrok.z3ctable.TablePage, ApplicationAwareView):
    """A table rendered as a page.
    """
    grok.baseclass()
        

class Index(Page, TabView):
    """A simple index for dolmen objects.
    """
    grok.order(-1)
    grok.baseclass()
    grok.name('index')
    grok.title(_(u"View"))
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)


class DefaultView(crud.Display, TabView, ApplicationAwareView):
    """The view per default for dolmen contents.
    """
    grok.order(-1)
    grok.name('index')
    grok.title(_(u"View"))
    grok.implements(IDisplayView)
    grok.require("dolmen.content.View")


class Form(PageForm, ApplicationAwareView):
    """A simple dolmen form.
    """
    grok.baseclass()
    cancellable(True)
    grok.require("dolmen.content.View")
    ignoreContext = True


class SubForm(composed.SubForm, ApplicationAwareView):
    """A SubForm base class with a nice template.
    """
    grok.baseclass()

    
class Add(crud.Add, ApplicationAwareView):
    """A generic form to add contents.
    """
    cancellable(True)
    

class Edit(crud.Edit, TabView, ApplicationAwareView):
    """A generic form to edit contents.
    """
    grok.order(20)
    grok.title(_(u"Edit"))
    grok.require("dolmen.content.Edit")
    cancellable(True)

    
__all__ = ['Page', 'Index', 'Form', 'TabView',
           'DefaultView', 'Add', 'Edit', 'SubForm',
           'TablePage', 'ApplicationAwareView']
