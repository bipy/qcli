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

try:
    import h5py
except ImportError:
    raise ImportError("h5py is required for functionality in this module")

VLENSTR = h5py.special_dtype(vlen=str)

class AutoExtendHDF5(object):
    """Allow for implicitly extendable datasets"""
    def __init__(self, f):
        self.f = f
        self._known_datasets = []

    def __del__(self):
        for n in self._known_datasets:
            self._finalize(n)

    def create_dataset(self, name, dtype):
        """Create a tracked dataset that will automatically reshape"""
        self.f.create_dataset(name, shape=(1,), maxshape=(None,), 
                              chunks=True, dtype=dtype)
        self.f[name].attrs['next_item'] = 0 # idx where next item can get written
        self._known_datasets.append(name)

    def extend(self, name, data, growth_factor=1):
        """Extend an automatically growable dataset"""
        n_data_items = len(data)
        next_item = self.f[name].attrs['next_item']

        # resize as needed
        if (next_item + n_data_items) >= self.f[name].size:
            new_size = next_item + n_data_items
            new_size += int(new_size * growth_factor)
            self.f[name].resize((new_size,))

        # store the data
        start = next_item
        end = next_item + len(data)
        self.f[name][start:end] = data
        self.f[name].attrs['next_item'] = end

    def _finalize(self, name):
        """Resize a dataset to its correct size"""
        actual_size = self.f[name].attrs.get('next_item', None)

        if actual_size is None:
            return

        self.f[name].resize((actual_size,))
        del self.f[name].attrs['next_item']
