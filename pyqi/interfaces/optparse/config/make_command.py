#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.optparse.output_handler import write_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pyqi.commands.make_command import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Basic Command",
        LongDesc="Create a basic Command with appropriate attribution",
        Ex='%prog -n example --credits "someone","and another person" -o "
            "example.py')
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('name'),
                   ShortName='n'),
    OptparseOption(Parameter=cmd_in_lookup('credits'),
                   Handler=string_list_handler,
                   Help='comma-separated list of authors'),
    OptparseOption(Parameter=cmd_in_lookup('test_code'),
                   Type=None, Action='store_true'),
    OptparseOption(Parameter=None,
                   Type='new_filepath',
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='output filepath to store generated Python code')
]

outputs = [
    ### InputName is used to tie this output to output-fp, which is an input...
    OptparseResult(Parameter=cmd_out_lookup('result'),
                   Handler=write_list_of_strings,
                   InputName='output-fp')
]
