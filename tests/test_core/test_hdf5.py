#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__credits__ = ["Daniel McDonald"]

import unittest

from unittest import TestCase, main
from os import remove
from numpy import array, hstack
from pyqi.core.hdf5 import AutoExtendHDF5

try:
    import h5py
    h5py_missing = False
except ImportError:
    h5py_missing = True

@unittest.skipIf(h5py_missing, "h5py is not present")
class HDF5AutoExtendTests(TestCase):
    def setUp(self):
        self.hdf5_file = h5py.File('_test_file.hdf5','w')
        self.obj = AutoExtendHDF5(self.hdf5_file)

    def tearDown(self):
        remove('_test_file.hdf5')

    def test_create_dataset(self):
        """Create something"""
        self.obj.create_dataset('test_group/test_ds', int)
        self.assertEqual(array([0],int), self.obj.f['test_group/test_ds'][:])
        self.assertEqual(self.obj._known_datasets, ['test_group/test_ds'])

    def test_extend(self):
        """Check the implicit resizing"""
        name = 'test_group/test_ds'
        fetch = lambda x: x[name][:x[name].attrs['next_item']]
        size = lambda x: x[name].size

        self.obj.create_dataset(name, int)
        ds1 = array([1,2,3,4])
        ds2 = array([5,10,20,50])
        ds3 = array([44,44,44,123,123])
        ds4 = array([1])

        self.obj.extend(name, ds1)
        self.assertTrue((fetch(self.obj.f) == ds1).all())
        self.assertEqual(self.obj.f[name].attrs['next_item'], 4)
        self.assertEqual(size(self.obj.f), 8)

        self.obj.extend(name, ds2)
        exp = hstack([ds1, ds2])
        obs = fetch(self.obj.f)
        self.assertTrue((obs == exp).all())
        self.assertEqual(self.obj.f[name].attrs['next_item'], 8)
        self.assertEqual(size(self.obj.f), 16)

        self.obj.extend(name, ds3)
        exp = hstack([ds1, ds2, ds3])
        obs = fetch(self.obj.f)
        self.assertTrue((obs == exp).all())
        self.assertEqual(self.obj.f[name].attrs['next_item'], 13)
        self.assertEqual(size(self.obj.f), 16)

        self.obj.extend(name, ds4)
        exp = hstack([ds1, ds2, ds3, ds4])
        obs = fetch(self.obj.f)
        self.assertTrue((obs == exp).all())
        self.assertEqual(self.obj.f[name].attrs['next_item'], 14)
        self.assertEqual(size(self.obj.f), 16)

    def test_finalize(self):
        """Make sure we can finalize a dataset"""
        name = 'test_group/test_ds'
        fetch = lambda x: x[name][:]
        size = lambda x: x[name].size
        self.obj.create_dataset(name, int)
        self.obj.extend(name, array([1,2,3]))
        self.obj.extend(name, array([1,2,3]))
        self.obj.extend(name, array([1,2,3]))
        self.obj.extend(name, array([1,2,3]))
        self.obj.extend(name, array([1,2,3]))

        self.assertEqual(size(self.obj.f), 24)
        exp = array([1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,0,0,0,0,0,0,0,0,0])
        obs = fetch(self.obj.f)
        self.assertTrue((obs == exp).all())

        self.obj._finalize(name)
        exp = array([1,2,3] * 5)
        obs = fetch(self.obj.f)
        self.assertTrue((obs == exp).all())

        self.assertFalse('next_item' in self.obj.f[name].attrs)

if __name__ == '__main__':
    main()
