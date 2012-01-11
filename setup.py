# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.layout'
version = '2.0a3'
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser >= 0.3a2',
    'cromlech.io >= 0.2a1',
    'cromlech.webob',
    'dolmen.app.security >= 2.0a1',
    'dolmen.forms.base >= 2.0b2',
    'dolmen.forms.crud >= 2.0b2',
    'dolmen.layout >= 0.2a2',
    'dolmen.menu',
    'dolmen.message',
    'dolmen.resources',
    'dolmen.tales',  # tales
    'dolmen.template',
    'dolmen.view >= 0.3a3',
    'dolmen.viewlet',
    'grokcore.component',
    'grokcore.security',
    'setuptools',
    'zope.interface',
    ]

tests_require = [
    'cromlech.browser [test] >= 0.3a2',
    'cromlech.io [test]',
    'dolmen.forms.base [test] >= 2.0b2',
    'dolmen.viewlet [test]',
    'grokcore.component',
    'zope.component',
    'zope.location',
    'zope.schema',
    'zope.testing',
    ]

setup(name = name,
      version = version,
      description = 'Layout and page models for Dolmen applications',
      long_description = readme + '\n\n' + history,
      keywords = 'Cromlech CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org/',
      download_url = '',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      test_suite="dolmen.app.layout",
      classifiers = [
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ])
