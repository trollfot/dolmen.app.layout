=================
dolmen.app.layout
=================

`dolmen.app.layout` provides ready-to-use components to get a fully
functional and extensively pluggable User Interface for a Dolmen
application (see `dolmen.app.site`).


About Dolmen
============

Dolmen is an application development framework based on Grok and ZTK
which also provides a CMS (Content Management System) out of the
box. Dolmen is being made with four main objectives in mind: easily
pluggable, rock solid and fast content type development, readability
and speed.


Getting started
===============

We import all the needed dependencies of the tests::

  >>> import grok
  >>> from dolmen.content import Content
  >>> from zope.component import getMultiAdapter 
  >>> from zope.publisher.browser import TestRequest
   
We import everything needed for the API verification::

  >>> from zope.interface import verify
  >>> from dolmen.app.layout import interfaces as API
 
We define and intanciate a Context object and a request for our tests
to come::

  >>> class Mammoth(Content):
  ...    grok.name('Furry Mammoth')

  >>> grok.testing.grok_component('mammoth', Mammoth)
  True

  >>> root = getRootFolder()
  >>> root['manfred'] = Mammoth()
  >>> manfred = root['manfred']

  >>> request = TestRequest()


Global interface
================
  
  >>> from dolmen.app.layout import master

  >>> API.IGlobalUI.extends(API.IContentProviders)
  True

  >>> API.IGlobalUI.providedBy(master)
  True
  >>> verify.verifyObject(API.IGlobalUI, master)
  True


Content providers
-----------------
 
Description
~~~~~~~~~~~

  >>> for name, attr in API.IContentProviders.namesAndDescriptions():
  ...   print "%s: %s" % (name, attr.getDoc())
  Footer: Viewlet manager for the bottom part of the body.
  AboveBody: Viewlet manager located above the main content.
  BelowBody: Viewlet manager located below the main content.
  Header: Viewlet manager involved in rendering the HTML head.
  Top: Viewlet manager for the top part of the body.


Layout
------

Description
~~~~~~~~~~~

  >>> interfaceDescription(API.IGlobalUI)
  Master: Base layout using all the `IContentProviders` components to build a coherent yet overridable rendering.



Contextual UI
=============

  >>> from dolmen.app.layout import viewlets

  >>> API.IContextualUI.providedBy(viewlets)
  True
  >>> verify.verifyObject(API.IContextualUI, viewlets)
  True

Description
-----------

  >>> interfaceDescription(API.IContextualUI)
  ContextualActions: Viewlet rendering contextual actions.
  FlashMessages: Viewlet displaying site-wide messages.


View components
===============

  >>> from dolmen.app.layout import models

Models
------

Models are base classes to be used in your own
classes. `dolmen.app.layout` provides a collections of ready-to-use
models::

  >>> API.IModels.providedBy(models)
  True
  >>> verify.verifyObject(API.IModels, models)
  True

Description
~~~~~~~~~~~

  >>> interfaceDescription(API.IModels)
  Index: Page showing as default view on an object.
  Form: Generic page form.
  SubForm: Generic sub-form, used in composed forms.
  TablePage: Page displaying a table.
  Page: Page embedded in a layout.


All the models are `megrok.layout.IPage` components, allowing them to
render inside a layout::

  >>> from megrok.layout import IPage

  >>> for name in list(API.IModels):
  ...    model = getattr(models, name)
  ...    print "%s:\t%s" % (name, IPage.implementedBy(model))
  Index:        True
  SubForm:	True
  TablePage: 	True
  Page: 	True
  Form: 	True


Default views
-------------

`dolmen.app.layout` registers some views, out-of-the-box, to allow you
to interact with your `dolmen.content` objects and your application::

  >>> API.IBaseViews.providedBy(models)
  True
  >>> verify.verifyObject(API.IBaseViews, models)
  True

Description
~~~~~~~~~~~

  >>> interfaceDescription(API.IBaseViews)
  Edit: Default edit form.
  DefaultView: Display form used as index.
  Add: Default add form.

Query
~~~~~

We can now test to see if our default views are retrieved::

  >>> view = getMultiAdapter((manfred, request), name="index")
  >>> view
  <dolmen.app.layout.models.DefaultView object at ...>

  >>> edit = getMultiAdapter((manfred, request), name="edit")
  >>> edit
  <dolmen.app.layout.models.Edit object at ...>

The add form is a bit different, as it relies on an adding view (see
`dolmen.forms.crud` and `dolmen.content` for more information):

  >>> from dolmen.forms.crud import Adder

  >>> adding = Adder(root, request)
  >>> adding
  <dolmen.forms.crud.addview.Adder object at ...>

  >>> adding.traverse("dolmen.app.layout.ftests.Mammoth", None)
  <dolmen.app.layout.models.Add object at ...>


Skins
=====

`dolmen.app.layout` provides a browser layer and a skin, to serve as a
base component for your own skins::

  >>> from dolmen.app.layout import skin

  >>> API.ISkin.providedBy(skin)
  True
  >>> verify.verifyObject(API.ISkin, skin)
  True

Description
-----------

  >>> interfaceDescription(API.ISkin)
  IBaseSkin: Skin providing the IBaseLayer. Can be applied directly or inherited.
  IBaseLayer: Layer used to register all the Dolmen centric view components.

Form compatibility
------------------

  >>> from megrok.z3cform.base import IFormLayer
  >>> skin.IBaseLayer.extends(IFormLayer)
  True


Menus
=====

  >>> from dolmen.app.layout import menus

  >>> API.IMenus.providedBy(menus)
  True
  >>> verify.verifyObject(API.IMenus, menus)
  True

Description
-----------

  >>> interfaceDescription(API.IMenus)
  MenuViewlet: Generic viewlet rendering a `IBrowserMenu`.
  ContextualMenu: Menu defining contextual actions.
  ContextualMenuEntry: Entry of the contextual actions menu.

Contextual menu
---------------

  >>> manager = master.Top(manfred, request, view)
  >>> manager
  <dolmen.app.layout.master.Top object at ...>

  >>> manager.update()
  >>> print manager.render()
  <dl id="contextual-actions" class="menu">
    <dt>Contextual actions</dt>
    <dd>
      <ul class="menu">
  <BLANKLINE>
        <li class="entry selected">
   	  <a title="View">View</a>
  	</li>
  <BLANKLINE>
  <BLANKLINE>
  	<li class="entry">
  	  <a href="http://127.0.0.1/manfred/edit" title="Edit">Edit</a>
   	</li>
  <BLANKLINE>
      </ul>
    </dd>
  </dl>
  <BLANKLINE>


Declaring a new entry::

  >>> class MyEntry(grok.View, menus.ContextualMenuEntry):
  ...   grok.context(Mammoth)
  ...   grok.title("A menu entry for tests")
  ...   def render(self):
  ...      return u"nothing to say"

  >>> grok.testing.grok_component('menu_entry', MyEntry)
  True

  >>> manager.update()
  >>> print manager.render()
  <dl id="contextual-actions" class="menu">
    <dt>Contextual actions</dt>
    <dd>
      <ul class="menu">
  <BLANKLINE>
  	<li class="entry">
  	  <a href="http://127.0.0.1/manfred/myentry"
        title="A menu entry for tests">A menu entry for tests</a>
  	</li>
  <BLANKLINE>
  <BLANKLINE>
  	<li class="entry selected">
  	  <a title="View">View</a>
  	</li>
  <BLANKLINE>
  <BLANKLINE>
  	<li class="entry">
  	  <a href="http://127.0.0.1/manfred/edit" title="Edit">Edit</a>
    	</li>
  <BLANKLINE>
      </ul>
    </dd>
  </dl>


Credits
=======

All Dolmen packages are sponsorised by NPAI (http://www.npai.fr)
