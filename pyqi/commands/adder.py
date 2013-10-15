#!/usr/bin/env python
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__version__ = "0.2-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

class Adder(Command):
    BriefDescription = "Add two numbers"
    LongDescription = "A simple Command that adds two numbers together"
    CommandIns = ParameterCollection([
        CommandIn(Name='x', DataType=float,
                  Description='Some number', Required=True),
        CommandIn(Name='y', DataType=float,
                  Description='Some other number', Required=True)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="result", DataType=float, 
                   Description="The result of the addition"),
    ])

    def run(self, **kwargs):
        return {'result':kwargs['x'] + kwargs['y']}

CommandConstructor = Adder
