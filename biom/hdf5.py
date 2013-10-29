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
import numpy as np
from scipy.sparse import coo_matrix
from biom.exception import TableException

class Table(object):
    """

    Some of the code in this class is taken and modified from other parts of
    the BIOM project. Credit goes to the contributing authors of that code
    where applicable.
    """

    axis_map = {'sample': 0, 'observation': 1}

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

    @property
    def shape(self):
        return self._data.shape

    @property
    def NumObservations(self):
        return self.shape[0]

    @property
    def NumSamples(self):
        return self.shape[1]

    @property
    def T(self):
        return self.transpose()

    def transpose(self):
        return self.__class__(self._data.transpose(), self.SampleIds[:],
                              self.ObservationIds[:], self.TableId)

    def sum(self, axis='whole'):
        if axis == 'whole':
            axis = None
        elif axis == 'sample':
            axis = 0
        elif axis == 'observation':
            axis = 1
        else:
            raise TableException("Unrecognized axis '%s'" % axis)

        matrix_sum = np.squeeze(np.asarray(self._data.sum(axis=axis)))

        if axis is not None and matrix_sum.shape == ():
            matrix_sum = matrix_sum.reshape(1)

        return matrix_sum
