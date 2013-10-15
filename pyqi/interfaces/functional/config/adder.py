#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interfaces.functional import Functional, FunctionalOption, \
        functional_factory
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pyqi.commands.adder import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [FunctionalOption(Parameter=cmd_in_lookup('x')),
          FunctionalOption(Parameter=cmd_in_lookup('y'))]
output_ = FunctionalOption(Parameter=cmd_out_lookup('result'))

interface_object = functional_factory(CommandConstructor, inputs, output_)
