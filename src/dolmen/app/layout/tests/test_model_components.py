# -*- coding: utf-8 -*-

import pytest
from cromlech.browser.testing import XMLDiff
from cromlech.io import IPublicationRoot
from cromlech.io.testing import TestRequest
from zope.testing.cleanup import cleanUp

from dolmen.app.layout import models
from dolmen.forms.base import testing
from dolmen.forms.crud import IFactoryAdding
from zope.component import getMultiAdapter
from zope.component.factory import Factory
from zope.interface import implements, Interface
from zope.location import Location
from zope.schema import TextLine


def setup_module(module):
    testing.grok("dolmen.layout.meta")
    testing.grok("dolmen.viewlet.meta")
    testing.grok("dolmen.app.layout.models")
    testing.grok("dolmen.app.layout.master")


def teardown_module(module):
    cleanUp()


class Folder(Location, dict):
    implements(IPublicationRoot)


class Adding(Location):
    implements(IFactoryAdding)

    __name__ = "add"
  
    def __init__(self, context, request, factory):
        self.context = context
        self.request = request
        self.factory = factory
        self.__parent__ = context
 
    def add(self, obj):
        id = str(len(self.context) + 1)
        self.context[id] = obj
        obj.__name__ = id
        obj.__parent__ = self.context
        return obj


def test_registered_models():
    folder = Folder()
    request = TestRequest()

    view = getMultiAdapter((folder, request), name="index")
    assert view.__class__ == models.DefaultView

    edit = getMultiAdapter((folder, request), name="edit")
    assert edit.__class__ == models.Edit

    adder = Adding(folder, request, Factory(object))
    add = getMultiAdapter((adder, request), name="add")
    assert add.__class__ == models.Add

    delete = getMultiAdapter((folder, request), name="delete")
    assert delete.__class__ == models.Delete


ADDFORM = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
 <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
   <head></head>
   <body>
     <div id="page">
       <div id="dolmen-site">
         <div id="dolmen-header"></div>
         <div id="dolmen-body">
 	   <div id="dolmen-above-body"></div>
 	   <div id="dolmen-inner-body">
            <form action="http://localhost/add/add" method="post"
                  enctype="multipart/form-data" id="form">
              <h1>Add</h1>
                <div class="actions">
                  <div class="action">
                    <input type="submit" id="form-action-add"
                           name="form.action.add" value="Add" class="action" />
                  </div>
                  <div class="action">
                    <input type="submit" id="form-action-cancel"
                           name="form.action.cancel" value="Cancel"
                           class="action" />
                  </div>
                </div>
              </form>
           </div>
 	   <div id="dolmen-below-body"></div>
         </div>
         <div id="dolmen-footer"></div>
       </div>
     </div>
   </body>
 </html>"""


def test_adding_form():
    folder = Folder()
    request = TestRequest()

    class MyContent(object):
        pass

    adder = Adding(folder, request, Factory(MyContent))
    add = getMultiAdapter((adder, request), name="add")
    assert not XMLDiff(str(add()), ADDFORM)


EDITFORM = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head></head>
  <body>
    <div id="page">
      <div id="dolmen-site">
        <div id="dolmen-header"></div>
        <div id="dolmen-body">
	  <div id="dolmen-above-body"></div>
	  <div id="dolmen-inner-body">
            <form action="http://localhost/item/edit" 
                  method="post"
                  enctype="multipart/form-data" id="form">
              <h1>Edit: item</h1>
              <div class="fields">
                <div class="field">
                  <label class="field-label"
                  for="form-field-myfield">My Field</label>
                  <span class="field-required">(required)</span>
                  <br />
                  <input type="text" id="form-field-myfield"
                         name="form.field.myfield" class="field"
                         value="Init value" />
                </div>
              </div>
              <div class="actions">
                <div class="action">
                  <input type="submit" id="form-action-update"
                         name="form.action.update" value="Update"
                         class="action" />
                </div>
                <div class="action">
                  <input type="submit" id="form-action-cancel"
                         name="form.action.cancel" value="Cancel"
                         class="action" />
                </div>
              </div>  
           </form>
         </div>
	<div id="dolmen-below-body"></div>
      </div>
      <div id="dolmen-footer"></div>
    </div>
  </div>
  </body>
</html>"""


def test_edit_form():

    class Schema(Interface):
        myfield = TextLine(title=u'My Field')
    
    class MyContent(Location):
        implements(Schema)
        myfield = u"Init value"

    folder = Folder()
    item = MyContent()
    request = TestRequest()

    item.__parent__ = folder
    item.__name__ = 'item'

    edit = getMultiAdapter((item, request), name="edit")
    assert(str(edit()), EDITFORM)
