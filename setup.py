# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.layout'
version = '2.0a1-dev'
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser',
    'cromlech.io',
    'dolmen.app.security',
    'dolmen.container',
    'dolmen.forms.base',
    'dolmen.forms.crud >= 2.0a1-dev',
    'dolmen.layout',
    'dolmen.location',
    'dolmen.menu',
    'dolmen.message',
    'dolmen.resources',
    'dolmen.template',
    'dolmen.view',
    'dolmen.viewlet',
    'grokcore.component',
    'grokcore.security',
    'setuptools',
    'zope.component',
    'zope.interface',
    ]

tests_require = [
    'cromlech.io',
    'cromlech.browser [test]',
    'dolmen.content',
    'dolmen.forms.base [test]',
    'grokcore.component',
    'zope.location',
    'zope.testing',
    ]

setup(name = name,
      version = version,
      description = 'Layout and page models for Dolmen applications',
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
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
