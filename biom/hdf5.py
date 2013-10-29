#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2011-2013, The BIOM Format Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2011-2013, The BIOM Format Development Team"
__credits__ = ["Jai Ram Rideout"]
__license__ = "BSD"
__url__ = "http://biom-format.org"
__version__ = "1.2.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

import h5py
from scipy.sparse import coo_matrix

class Table(object):
    @classmethod
    def fromFile(cls, table_fp):
        table_f = h5py.File(table_fp, 'r')
        obs_ids = table_f['rows'].value
        sample_ids = table_f['columns'].value
        table_id = table_f.attrs['id']

        data_grp = table_f['data']
        matrix = coo_matrix((data_grp['values'].value,
                            (data_grp['rows'].value,
                             data_grp['columns'].value)),
                            shape=table_f.attrs['shape'])
        table_f.close()

        return cls(matrix, obs_ids, sample_ids, table_id)

    def __init__(self, data, ObservationIds, SampleIds, TableId=None):
        self._data = data
        self.ObservationIds = ObservationIds
        self.SampleIds = SampleIds
        self.TableId = TableId
