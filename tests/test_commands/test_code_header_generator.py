#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Jai Ram Rideout", "Adam Robbins-Pianka"]

from unittest import TestCase, main
from pyqi.commands.code_header_generator import CodeHeaderGenerator

class CodeHeaderGeneratorTests(TestCase):
    def setUp(self):
        """Set up a CodeHeaderGenerator instance to use in the tests."""
        self.cmd = CodeHeaderGenerator()

    def test_run(self):
        """Correctly generates header with and without credits."""
        obs = self.cmd(credits=['bob'])
        self.assertEqual(obs.keys(), ['result'])

        obs = obs['result']
        self.assertEqual('\n'.join(obs), exp_header1)

        # With more than 1 credit.
        obs = self.cmd(credits=['bob', 'another person',
            'another another person'])
        self.assertEqual(obs.keys(), ['result'])

        obs = obs['result']
        self.assertEqual('\n'.join(obs), exp_header2)


exp_header1 = """#!/usr/bin/env python
from __future__ import division

__credits__ = ["bob"]
"""

exp_header2 = """#!/usr/bin/env python
from __future__ import division

__credits__ = ["bob", "another person", "another another person"]
"""


if __name__ == '__main__':
    main()
