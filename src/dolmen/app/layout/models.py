# -*- coding: utf-8 -*-

import grok
import megrok.menu
import megrok.layout
import megrok.z3ctable
import dolmen.content as content

from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from z3c.flashmessage.interfaces import IMessageSource

from megrok.z3cform import composed
from menhir.library.tablesorter import SimpleTableSorter

from dolmen.forms import crud
from dolmen.app.site import IDolmen
from dolmen.forms.base import PageForm, cancellable
from dolmen.app.layout import ContentActions, IDisplayView, ISortable

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

    
class View(Page):
    """An alternative view for an object.
    """
    grok.baseclass()
    megrok.menu.menuitem('display')

    
class TabView(Page):
    """A contextual tab.
    """
    grok.baseclass()
    megrok.menu.menuitem(ContentActions)


class TablePage(megrok.z3ctable.TablePage, ApplicationAwareView):
    """A contextual tab.
    """
    grok.baseclass()

    def update(self):
        if ISortable.providedBy(self):
            SimpleTableSorter.need()
            if "table" in self.cssClasses:
                if not "sortable" in self.cssClasses['table']:
                    self.cssClasses['table'] += u" sortable"
        megrok.z3ctable.TablePage.update(self)
        

class Index(Page):
    """A simple index for dolmen objects.
    """
    grok.baseclass()
    grok.name('index')
    grok.title(_(u"View"))
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)
    megrok.menu.menuitem(ContentActions, order=10)


class DefaultView(crud.Display, ApplicationAwareView):
    """The view per default of the non 'dynamic layout' objects.
    """
    grok.name('index')
    grok.title(_(u"View"))
    grok.require("dolmen.content.View")
    grok.implements(IDisplayView)
    megrok.menu.menuitem(ContentActions, order=10)


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
    

class Edit(crud.Edit, ApplicationAwareView):
    """A generic form to edit contents.
    """
    cancellable(True)
    grok.title(_(u"Edit"))
    grok.require("dolmen.content.Edit")
    megrok.menu.menuitem(ContentActions, order=20)


__all__ = ['Page', 'View', 'Form', 'TabView',
           'Index', 'Add', 'Edit', 'SubForm',
           'TablePage', 'ApplicationAwareView']
