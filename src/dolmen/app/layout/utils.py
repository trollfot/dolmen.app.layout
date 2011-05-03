# -*- coding: utf-8 -*-

import os.path
from dolmen.template import ITemplate
from zope.component import queryMultiAdapter


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def template_path(filename):
    return os.path.join(TEMPLATES_DIR, filename)


def queryViewTemplate(view):
    """Retuns a template associated to a view, or None.
    """
    return queryMultiAdapter((view, view.request), ITemplate)
