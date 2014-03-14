#!/usr/bin/env python
from __future__ import division

__credits__ = []

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pyqi.commands.make_package import CommandConstructor

# If you need access to input or output handlers provided by pyqi, consider
# importing from the following modules:
# pyqi.core.interfaces.optparse.input_handler
# pyqi.core.interfaces.optparse.output_handler
# pyqi.interfaces.optparse.input_handler
# pyqi.interfaces.optparse.output_handler

# Convenience function for looking up parameters by name.
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

# Examples of how the command can be used from the command line using an
# optparse interface.
usage_examples = [
    OptparseUsageExample(ShortDesc="Stub out a pyqi package",
                         LongDesc="Construct the base structure for a pyqi package",
                         Ex="%prog --pkg-base=$HOME/gitables --pkg-name=FTW --author=foo --email=bar --bar some_file --pyqi-package"),
    OptparseUsageExample(ShortDesc="Stub out a non-pyqi package",
                         LongDesc="Construct the base structure for a regular package",
                         Ex="%prog --pkg-base=$HOME/gitables --pkg-name=FTW --author=foo --email=bar --bar some_file"),
]

# inputs map command line arguments and values onto Parameters. It is possible
# to define options here that do not exist as parameters, e.g., an output file.
inputs = [
    OptparseOption(Parameter=cmd_in_lookup('author'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('email'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('pkg_base'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('pkg_name'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('url'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   ),
    OptparseOption(Parameter=cmd_in_lookup('pyqi_package'),
                   Type=None,
                   Action='store_true',
                   Handler=None,
                   ShortName=None)
]

outputs = []
