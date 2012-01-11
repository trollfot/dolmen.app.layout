# -*- coding: utf-8 -*-

import os
from dolmen.template import TALTemplate

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def get_template(filename):
    return TALTemplate(os.path.join(TEMPLATES_DIR, filename))


from dolmen.app.layout.interfaces import IDisplayView
from dolmen.app.layout.menus import *
from dolmen.app.layout.master import *
from dolmen.app.layout.models import *
from dolmen.app.layout.viewlets import *

# APIs
from zope.interface import moduleProvides
from dolmen.app.layout.interfaces import IDolmenLayoutAPI

moduleProvides(IDolmenLayoutAPI)
__all__ = list(IDolmenLayoutAPI) + ['IDisplayView']
