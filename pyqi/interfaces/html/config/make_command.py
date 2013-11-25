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
__credits__ = ["Evan Bolyen"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.interfaces.html import (HTMLInputOption, HTMLDownload, HTMLPage)
from pyqi.core.interfaces.html.input_handler import string_list_handler, string_to_true_false
from pyqi.core.interfaces.html.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from pyqi.commands.make_command import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [
    HTMLInputOption(Parameter=cmd_in_lookup('name')),
    HTMLInputOption(Parameter=cmd_in_lookup('author')),
    HTMLInputOption(Parameter=cmd_in_lookup('email')),
    HTMLInputOption(Parameter=cmd_in_lookup('license')),
    HTMLInputOption(Parameter=cmd_in_lookup('copyright')),
    HTMLInputOption(Parameter=cmd_in_lookup('version'), Name='command-version'),
    HTMLInputOption(Parameter=cmd_in_lookup('credits'),
                   Handler=string_list_handler,
                   Help='comma-separated list of other authors'),
    HTMLInputOption(Parameter=cmd_in_lookup('test_code'),
                   Type="multiple_choice",
                   Choices=["True", "False"],
                   Default="False",
                   Handler=string_to_true_false,
                   Help='Should a stubbed out python test file be generated instead'),
    HTMLInputOption(Parameter=None,
                   Name='download-file',
                   Required=True,
                   Help='The name of the file to download which conatins generated Python code. (e.g. my_command)')
]

output = HTMLDownload(Parameter=cmd_out_lookup('result'),
                   Handler=newline_list_of_strings,
                   FilenameLookup='download-file',
                   FileExtension='.py')

#Comment out the above and uncomment the below for an example of a page.

#     HTMLPage(Parameter=cmd_out_lookup('result'),
#              Handler=newline_list_of_strings) 
    

