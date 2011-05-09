# -*- coding: utf-8 -*-

# tests imports
from grokcore.component import testing
from cromlech.browser.testing import TestView, XMLDiff
from cromlech.io.testing import TestRequest
from zope.testing.cleanup import cleanUp

# Components and utilities
from cromlech.browser import IViewSlot
from dolmen.app.layout import models, master
from zope.component import getAdapters
from zope.interface import implements
from zope.location import Location


def setup_module(module):
    testing.grok("dolmen.location")
    testing.grok("dolmen.layout.meta")
    testing.grok("dolmen.viewlet.meta")
    testing.grok("dolmen.app.layout.master")


def teardown_module(module):
    cleanUp()


EXPECTED = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
 <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
   <head></head>
   <body>
     <div id="page">
       <div id="dolmen-site">
         <div id="dolmen-header"></div>
         <div id="dolmen-body">
 	   <div id="dolmen-above-body"></div>
 	   <div id="dolmen-inner-body">My page is nice</div>
 	   <div id="dolmen-below-body"></div>
         </div>
         <div id="dolmen-footer"></div>
       </div>
     </div>
   </body>
 </html>"""


def test_master_layout():
    """We test that the layout respond as we wish.
    """
    context = Location()
    request = TestRequest()

    class MyPage(models.Page):
        def render(self):
            return "My page is nice"
    
    view = MyPage(context, request)
    assert not XMLDiff(str(view()), EXPECTED)
