# -*- coding: utf-8 -*-

import os.path
import zope.i18n
from dolmen.template import ITemplate
from dolmen.layout import query_layout
from cromlech.browser.interfaces import ILayout
from zope.component import queryMultiAdapter


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def template_path(filename):
    return os.path.join(TEMPLATES_DIR, filename)


def queryViewTemplate(view):
    """Retuns a template associated to a view, or None.
    """
    return queryMultiAdapter((view, view.request), ITemplate)


def layout_view_renderer(view, *args, **kwargs):
    view.update(*args, **kwargs)
    if not view.response.status_int in [301, 302]:
        name = getattr(view, 'layout_name', u'')
        layout = query_layout(
            view.request, view.context, ILayout, name=name)
        return layout(view.render(*args, **kwargs), view=view)
    return view.response


def layout_form_renderer(form, *args, **kwargs):
    form.update(*args, **kwargs)

    if not form.response.status_int in (302, 303):
        if form.i18nLanguage is None:
            # We want some i18n information
            form.i18nLanguage = zope.i18n.negotiate(form.request)

        # We now extract and process the form.
        form.updateForm()

        if not form.response.status_int in [301, 302]:
            # If no redirect happened, we render.
            name = getattr(form, 'layout_name', u'')
            layout = query_layout(
                form.request, form.context, ILayout, name=name)
            return layout(form.render(*args, **kwargs), view=form)

    return form.response
