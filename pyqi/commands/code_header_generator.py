#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Jai Ram Rideout", "Daniel McDonald", "Adam Robbins-Pianka"]

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

header_format = """#!/usr/bin/env python
from __future__ import division

__credits__ = [%(credits)s]
"""

class CodeHeaderGenerator(Command):
    BriefDescription = "Generate header code for use in a Python file"
    LongDescription = ("Generate valid Python code containing header "
                       "information, such as author, email address, "
                       "maintainer, version, etc.. This code can be placed at "
                       "the top of a Python file.")

    CommandIns = ParameterCollection([
        CommandIn(Name='credits', DataType=list,
                  Description='list of authors',
                  Required=True, Default=None)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=list,
                   Description='the resulting header')])

    def run(self, **kwargs):
        # Build a string formatting dictionary for the file header.
        head = {}

        credits = kwargs['credits']

        def f(x):
            """Returns a double-quoted version of input"""
            return '"%s"' % x

        head['credits'] = ', '.join(map(f, credits))

        return {'result': (header_format % head).split('\n')}

CommandConstructor = CodeHeaderGenerator
