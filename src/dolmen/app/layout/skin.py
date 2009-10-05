# -*- coding: utf-8 -*-

from grokcore.view import skin
from z3c.form.interfaces import IFormLayer
from zope.publisher.interfaces import browser


class IDolmenBaseLayer(IFormLayer, browser.IDefaultBrowserLayer):
    """Base layer for a dolmen application
    """


class IDolmenBaseSkin(IDolmenBaseLayer, browser.IBrowserSkinType):
    """A very basic skin, implementing the needed layers to have a fully
    functional display : forms and other components.
    """
    skin("basic_dolmen_skin")
