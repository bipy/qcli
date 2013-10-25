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

from unittest import TestCase, main
from pyqi.core.interfaces.functional import (Functional, FunctionalOption,
                                             functional_factory)
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Command, CommandIn, CommandOut, ParameterCollection

class FunctionalInterfaceTests(TestCase):
    def setUp(self):
        self.interface = functionally_fabulous()

    def test_init(self):
        with self.assertRaises(IncompetentDeveloperError):
            _ = Functional()

    def test_validate_inputs(self):
        with self.assertRaises(ValueError):
            _ = self.interface._the_in_validator(None)

    def test_validate_outputs(self):
        pass

    def test_input_handler(self):
        with self.assertRaises(ValueError):
            _ = self.interface._input_handler(1)
        
        with self.assertRaises(ValueError):
            _ = self.interface._input_handler(1, 2)

        exp = {'a':1, 'b':2.0}
        obs = self.interface._input_handler(1, 2.0)
        self.assertEqual(obs, exp)

    def test_output_handler(self):
        exp = 10
        obs = self.interface._output_handler({'x':10,'y':20,'z':30})
        self.assertEqual(obs, exp)

class functionally_ghetto(Command):
    CommandIns = ParameterCollection([
        CommandIn('a',int,'b'),
        CommandIn('b',float,'c'),
        CommandIn('c',str,'c')])
    CommandOuts = ParameterCollection([CommandOut('x',int,'b')])

    def run(self, **kwargs):
        return {'x':a*10}

class functionally_fabulous(Functional):
    CommandConstructor = functionally_ghetto

    def _get_inputs(self):
        return [FunctionalOption(Type=int,
                    Parameter=self.CommandConstructor.CommandIns['a']),
                FunctionalOption(Type=float,
                    Parameter=self.CommandConstructor.CommandIns['b'])]

    def _get_usage_examples(self):
        return []

    def _get_outputs(self):
        return [FunctionalOption(Type=int,
                    Parameter=self.CommandConstructor.CommandOuts['x'])]

    def _get_version(self):
        return "foo"

if __name__ == '__main__':
    main()


