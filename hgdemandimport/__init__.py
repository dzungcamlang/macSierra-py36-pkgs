# hgdemandimport - global demand-loading of modules for Mercurial
#
# Copyright 2017 Facebook Inc.
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

'''demandimport - automatic demand-loading of modules'''

# This is in a separate package from mercurial because in Python 3,
# demand loading is per-package. Keeping demandimport in the mercurial package
# would disable demand loading for any modules in mercurial.



import sys

if sys.version_info[0] >= 3:
    from . import demandimportpy3 as demandimport
else:
    from . import demandimportpy2 as demandimport

# Extensions can add to this list if necessary.
ignore = [
    '__future__',
    '_hashlib',
    # ImportError during pkg_resources/__init__.py:fixup_namespace_package
    '_imp',
    '_xmlplus',
    'fcntl',
    'nt', # pathlib2 tests the existence of built-in 'nt' module
    'win32com.gen_py',
    'win32com.shell', # 'appdirs' tries to import win32com.shell
    '_winreg', # 2.7 mimetypes needs immediate ImportError
    'pythoncom',
    # imported by tarfile, not available under Windows
    'pwd',
    'grp',
    # imported by profile, itself imported by hotshot.stats,
    # not available under Windows
    'resource',
    # this trips up many extension authors
    'gtk',
    # setuptools' pkg_resources.py expects "from __main__ import x" to
    # raise ImportError if x not defined
    '__main__',
    '_ssl', # conditional imports in the stdlib, issue1964
    '_sre', # issue4920
    'rfc822',
    'mimetools',
    'sqlalchemy.events', # has import-time side effects (issue5085)
    # setuptools 8 expects this module to explode early when not on windows
    'distutils.msvc9compiler',
    '__builtin__',
    'builtins',
    'urwid.command_map', # for pudb
    ]

_pypy = '__pypy__' in sys.builtin_module_names

if _pypy:
    ignore.extend([
        # _ctypes.pointer is shadowed by "from ... import pointer" (PyPy 5)
        '_ctypes.pointer',
    ])

demandimport.init(ignore)

# Re-export.
isenabled = demandimport.isenabled
enable = demandimport.enable
disable = demandimport.disable
deactivated = demandimport.deactivated
