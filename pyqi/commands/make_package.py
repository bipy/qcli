#!/usr/bin/env python
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "pyqi, copyright 2014"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

import os
from pyqi import __version__  # note, pyqi has not been vermanized
from pyqi.core.command import (Command, CommandIn, ParameterCollection)
from pyqi.util import pyqi_system_call

PKG_INIT = """#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2014, The biocore Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from verman import Version
%(pkg_name)s_version = Version("%(pkg_name)s", 0, 1, 0, releaselevel="dev", init_file=__file__)
__version__ = %(pkg_name)s_version.mmm
"""


COPYING = """=============================
 The %(pkg_name)s licensing terms
=============================

%(pkg_name)s is licensed under the terms of the Modified BSD License (also known as
New or Revised BSD), as follows:

Copyright (c) 2014, biocore Development Team %(email)s

All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name BiPy nor the names of its contributors may be used to
      endorse or promote products derived from this software without specific
      prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE BIPY DEVELOPMENT TEAM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The biocore Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
"""

README = """%(pkg_name)s
===============

A simple package that does all the awesome
"""

CHANGELOG = """%(pkg_name)s ChangeLog
===================

%(pkg_name)s 0.1.0-dev
--------------------

* initial creation of teh awesome
"""

SETUP = """#!/usr/bin/env python

from setuptools import setup
from glob import glob
from %(pkg_name)s import %(pkg_name)s_version
import sys

__author__ = "%(author)s"
__copyright__ = "Copyright 2014"
__credits__ = ["%(author)s"]
__license__ = "BSD"
__version__ = %(pkg_name)s_version.mmm
__maintainer__ = "%(author)s"
__email__ = "%(email)s"

# PyPI's list of classifiers can be found here by Googling:
# "pypi list of classifiers"
classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: OS Independent",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X"
]

# Verify Python version
ver = '.'.join(map(str, [sys.version_info.major, sys.version_info.minor]))
if ver not in ['2.7']:
    sys.stderr.write("Only Python >=2.7 and <3.0 is supported.")
    sys.exit(1)

short_description = "Doing things"
long_description = "Committing acts of awesome"

setup(name='%(pkg_name)s',
      version=__version__,
      license=__license__,
      description=short_description,
      long_description=long_description,
      author=__maintainer__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__email__,
      url='%(url)s',
      packages=['%(pkg_name)s'],
      scripts=glob('scripts/*'),
      install_requires=[%(pyqi_pip_requires)s],
      extras_require={'test': ['nose >= 0.10.1',
                               'tox >= 1.6.1']
                     },
      classifiers=classifiers
      )
"""

MANIFEST = """include README.md
include COPYING.txt
include README.md
include ChangeLog.md

graft %(pkg_name)s
graft scripts
graft doc

global-exclude *.pyc
global-exclude *.pyo
global-exclude .git
"""

MAKEFILE = """#
# Based on Makefile from https://github.com/mitsuhiko/flask/blob/master/Makefile
# at SHA-1: afd3c4532b8625729bed9ed37a3eddd0b7b3b5a9
#
.PHONY: clean-pyc test upload-docs docs

all: clean-pyc clean-docs test tox-test docs

clean: clean-pyc clean-docs

test:
    nosetests

tox-test:
    tox

release_test:
    pyqi make-release --package-name=%(pkg_name)s

release_real:
    pyqi make-release --package-name=%(pkg_name)s --real-run

clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +

docs:
    $(MAKE) -C doc html

clean-docs:
    $(MAKE) -C doc clean

love:
    @echo not war
"""

PYQI_DRIVER = """#!/bin/sh

exec pyqi --driver-name %(pkg_name)s --command-config-module %(pkg_name)s.interfaces.optparse.config -- "$@"
"""

def touch(path):
    f = open(path, 'w')
    f.close()

def write_file(fname, payload):
    if os.path.exists(fname):
        raise IOError("%s exists!" % fname)

    with open(fname, 'w') as f:
        f.write(payload)

class MakePackage(Command):
    BriefDescription = "Stub out a package"
    LongDescription = "Create the basic directory structure for a Python package"
    CommandIns = ParameterCollection([
        CommandIn(Name='pkg_name', DataType=str,
                  Description='name of the package', Required=True),
        CommandIn(Name='pkg_base', DataType=str,
                  Description='base path for package', Required=True),
        CommandIn(Name='email', DataType=str,
                  Description='contact email', Required=True),
        CommandIn(Name='author', DataType=str,
                  Description='package author', Required=True),
        CommandIn(Name='url', DataType=str,
                  Description='package URL', Required=False, Default=''),
        CommandIn(Name='pyqi_package', DataType=bool,
                  Description='Flag to indicate if this is a pyqi package',
                  Required=False, Default=False)
    ])

    CommandOuts = ParameterCollection([])

    _formatted_base_writes = [('COPYING.txt', COPYING),
                              ('README.md', README),
                              ('setup.py', SETUP),
                              ('ChangeLog.md', CHANGELOG),
                              ('MANIFEST.in', MANIFEST),
                              ('Makefile', MAKEFILE)]

    def _create_directories_pyqi(self, pkg_name):
        os.makedirs('%s/commands' % pkg_name)
        os.makedirs('%s/interfaces/optparse/config' % pkg_name)
        os.makedirs('doc')
        os.makedirs('scripts')
        os.makedirs('tests')

    def _create_directories_nonpyqi(self, pkg_name):
        os.makedirs('%s' % pkg_name)
        os.makedirs('doc')
        os.makedirs('scripts')
        os.makedirs('tests')

    def _create_empty_inits(self, pkg_name):
        touch('%s/commands/__init__.py' % pkg_name)
        touch('%s/interfaces/__init__.py' % pkg_name)
        touch('%s/interfaces/optparse/__init__.py' % pkg_name)
        touch('%s/interfaces/optparse/config/__init__.py' % pkg_name)

    def _create_pkg_init(self, pkg_name):
        payload = PKG_INIT % {'pkg_name': pkg_name}
        write_file('%s/__init__.py' % pkg_name, payload)

    def _create_pyqi_driver(self, pkg_name):
        payload = PYQI_DRIVER % {'pkg_name': pkg_name}
        write_file('scripts/%s' % pkg_name, payload)
        os.chmod('scripts/%s' % pkg_name, 0755)

    def _create_git(self):
        init_cmd = ['git', 'init', '--quiet']
        add_cmd = ['git', 'add', '*']
        commit_cmd = ['git', 'commit', '-qm', '"initial creation"']

        so, se, ret = pyqi_system_call(init_cmd, shell=False)
        so, se, ret = pyqi_system_call(add_cmd, shell=False)
        so, se, ret = pyqi_system_call(commit_cmd, shell=False)

    def run(self, **kwargs):
        cwd = os.getcwd()
        os.chdir(kwargs['pkg_base'])
        os.mkdir(kwargs['pkg_name'])
        os.chdir(kwargs['pkg_name'])

        if kwargs['pyqi_package']:
            self._create_directories_pyqi(kwargs['pkg_name'])
            self._create_empty_inits(kwargs['pkg_name'])
            self._create_pyqi_driver(kwargs['pkg_name'])
            kwargs['pyqi_pip_requires'] = '"pyqi == %s"' % __version__
        else:
            self._create_directories_nonpyqi(kwargs['pkg_name'])
            kwargs['pyqi_pip_requires'] = ""

        self._create_pkg_init(kwargs['pkg_name'])

        for fname, formatted_str in self._formatted_base_writes:
            write_file(fname, formatted_str % kwargs)

        self._create_git()

        os.chdir(cwd)
        return {}

CommandConstructor = MakePackage
