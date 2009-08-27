# -*- coding: utf-8 -*-

from zope.interface import Interface


class ISortable(Interface):
    """A marker interface defining a sortable element.
    """

class IDisplayView(Interface):
    """Defines the visualisation view of an object. More specifically, it
    defines any view that display the object in a non-editable way.
    """
