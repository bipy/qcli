#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen", "Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.optparse.output_handler import write_list_of_strings
from pyqi.core.command import make_command_in_collection_lookup_f, make_command_out_collection_lookup_f
from pyqi.commands.serve_html_interface import CommandConstructor

cmdin_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmdout_lookup = make_command_out_collection_lookup_f(CommandConstructor)

def printer(result_key, data, option_value=None):
    print ""
    print data

usage_examples = [
    OptparseUsageExample(ShortDesc="Basic Command",
                         LongDesc="Create a basic Command with appropriate attribution",
                         Ex='%prog -n example -a "some author" -c "Copyright 2013, The pyqi project" -e "foo@bar.com" -l BSD --command-version "0.1" --credits "someone else","and another person" -o example.py')
]

inputs = [
    OptparseOption(Parameter=cmdin_lookup('port'),
                   ShortName='p',
                   Type='int',
                   Required=False,
                   Help='Port to run the server on.'),

    OptparseOption(Parameter=cmdin_lookup('interface_module'),
                   ShortName='m',
                   Type='str',
                   Required=True,
                   Help='The python interface module to run the server on.')
]

outputs = [
    OptparseResult(Parameter=cmdout_lookup('result'),
                   Handler=printer)
]