# -*- coding: utf-8 -*-

from zope.interface import verify
from dolmen.app.layout import menus, master, viewlets, models
from dolmen.app.layout import interfaces as API


def getAttrs(iface):
    return [name for name, attr in iface.namesAndDescriptions()]


def test_menu():
    assert API.IMenus.providedBy(menus)
    assert verify.verifyObject(API.IMenus, menus)
    assert getAttrs(API.IMenus) == (
        ['ContextualMenu', 'MenuViewlet'])


def test_contextual_ui():
    assert API.IContextualUI.providedBy(viewlets)
    assert verify.verifyObject(API.IContextualUI, viewlets)
    assert getAttrs(API.IContextualUI) == (
        ['ContextualActions', 'Resource', 'FlashMessages'])


def test_content_providers():
    assert API.IGlobalUI.extends(API.IContentProviders)
    assert API.IGlobalUI.providedBy(master)
    assert verify.verifyObject(API.IGlobalUI, master)
    assert getAttrs(API.IGlobalUI) == (
        ['Master'])


def test_modules():
    assert API.IBaseViews.providedBy(models)
    assert verify.verifyObject(API.IBaseViews, models)
    assert getAttrs(API.IBaseViews) == (
        ['Edit', 'Add', 'DefaultView', 'Delete'])
