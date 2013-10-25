#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Daniel McDonald"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interface import Interface, InterfaceOption
from pyqi.core.factory import general_factory
from types import NoneType
from itertools import izip

class Functional(Interface):
    """Provide a functional interface for pyqi Commands

    This interface requires that a wrapped Command only return a single
    described value, and only take (as in_) a single argument. However,
    kwargs are still allowed, so the following is fine:

    result = g(f(x, y=5), z=10)

    As is:

    result = map(f, [x,y,z])
    """
    def _validate_usage_examples(self, foo):
        pass

    def _the_in_validator(self, in_):
        if isinstance(in_, NoneType):
            raise ValueError("No input specified!")

    def _input_handler(self, in_, *args, **kwargs):
        interface_ins = self._get_inputs()
        args = list(args)
        args.insert(0, in_)

        if len(args) != len(interface_ins):
            raise ValueError("Have %d arguments but expect %d!" % (len(args), 
                                    len(interface_ins)))

        for interface_in, input_ in izip(interface_ins, args):
            if not isinstance(input_, interface_in.Type):
                raise ValueError("Input %s doesn't appear to be the correct"\
                                 "type!" % interface_in.Name)

            # assume kwargs values are all in memory already
            kwargs[interface_in.Name] = input_
        return kwargs

    def _the_out_validator(self, result):
        pass

    def _output_handler(self, result):
        """Return only the specified output"""
        interface_out = self._get_outputs()[0]
        return result[interface_out.Name]

class FunctionalOption(InterfaceOption):
    """Describe the required Parameter for input and output

    An instance of this object is used to describe the input parameter 
    (CommandIn), and an instance of this object is used to describe the
    output parameter (CommandOut) of interest.
    """
    def __init__(self, **kwargs):
        super(FunctionalOption, self).__init__(**kwargs)
        self.Type = self.Parameter.DataType

def functional_factory(command_constructor, inputs, output):
    """Optparse command line interface factory

    command_constructor - a subclass of ``Command``
    inputs  - config ``input_`` list of ``FunctionalOption``s 
    outputs - config ``output_`` ``FunctionalOption``
    version - config ``__version__`` (a version string)
    """
    return general_factory(command_constructor, None, inputs,
                           [output], None, Functional)
