#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.interface import Interface
from z3c.form.interfaces import IButton, IButtonForm, IHandlerForm


class ISortable(Interface):
    """A marker interface defining a sortable element.
    """

class IDisplayView(Interface):
    """Defines the visualisation view of an object. More specifically, it
    defines any view that display the object in a non-editable way.
    """

class IForm(IButtonForm, IHandlerForm):
    """Defines a modifying view of an object. It is a form, inheriting from
    the z3c.form components.
    """

class ICancelButton(IButton):
    """A button to cancel a form.
    """

class IUncancellableForm(IForm):
    """Marker interface for forms that can't be cancelled.
    """
