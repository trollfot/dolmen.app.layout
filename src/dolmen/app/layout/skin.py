# -*- coding: utf-8 -*-

from grokcore.view import skin
from zope.publisher.interfaces import browser
from z3c.form.interfaces import IFormLayer


class IDolmenBaseLayer(IFormLayer, browser.IDefaultBrowserLayer):
    """Base layer for a dolmen application
    """


class IBlankDolmenSkin(IDolmenBaseLayer, browser.IBrowserSkinType):
    """A skin with light-blue tones. Very sober yet effective.
    """
    skin("blank")
