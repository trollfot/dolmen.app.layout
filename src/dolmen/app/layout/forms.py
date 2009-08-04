# -*- coding: utf-8 -*-

"""
z3c.form allows to define buttons as multi adapters, in order to have
fully customizable forms.
"""

import grokcore.component as grok
from megrok.z3cform import button
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import AbsoluteURL
from dolmen.app.layout.interfaces import ICancelButton
from dolmen.app.layout.interfaces import IForm, IUncancellableForm

_ = MessageFactory("dolmen")


class CancelButton(button.Button):
    """A cancel button.
    """
    grok.implements(ICancelButton)


class FormActions(button.ButtonActions, grok.MultiAdapter):
    grok.adapts(IForm, Interface, Interface)

    def update(self):
        if not IUncancellableForm.providedBy(self.form):
            self.form.buttons = button.Buttons(
                self.form.buttons,
                CancelButton('cancel', _(u'Cancel'), accessKey=u'c')
                )
        super(FormActions, self).update()


class AddActionHandler(button.ButtonActionHandler, grok.MultiAdapter):
    grok.adapts(IForm, Interface, Interface, button.ButtonAction)

    def __call__(self):
        if not IUncancellableForm.providedBy(self.form):
            if self.action.name == 'form.buttons.cancel':
                self.form.redirect(AbsoluteURL(self.form.context, self.request))
                return
        return super(AddActionHandler, self).__call__()

