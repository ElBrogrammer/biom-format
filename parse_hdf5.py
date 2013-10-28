#!/usr/bin/env python
from __future__ import division

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, BIOM-Format Project"
__credits__ = ["Jai Ram Rideout"]
__license__ = "GPL"
__url__ = "http://biom-format.org"
__version__ = "1.2.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

import sys
import h5py
import numpy
from scipy.sparse import coo_matrix

from biom import get_sparse_backend
from biom.csmat import CSMat
from biom.table import table_factory, SparseOTUTable

SparseObj, to_sparse, dict_to_sparseobj, list_dict_to_sparseobj, \
        list_nparray_to_sparseobj, nparray_to_sparseobj, \
        list_list_to_sparseobj = get_sparse_backend()

in_fp = sys.argv[1]

print "Opening HDF5 file...",
biom_f = h5py.File(in_fp, 'r')
print "Done"

print "Loading observation IDs...",
obs_ids = biom_f['rows'].value
print "Done"

print "Loading sample IDs...",
sample_ids = biom_f['columns'].value
print "Done"

print "Loading data...",
data = biom_f['data'].value
#print data[0]
#print data[2]
#data = biom_f['data'].value.tolist()
I = data[:,0]
J = data[:,1]
V = data[:,2]
table = coo_matrix((V, (I, J)), shape=biom_f.attrs['shape'])
table = table.tocsr()
print "Done"

#mat = CSMat(*biom_f.attrs['shape'])
#mat.bulkCOOUpdate(data[:,0], data[:,1], data[:,2])

#data = list_list_to_sparseobj(data, shape=biom_f.attrs['shape'])
#table = SparseOTUTable(data, sample_ids, obs_ids)
#table = table_factory(data, sample_ids, obs_ids, shape=biom_f.attrs['shape'])

print table[0,0]
print table[0,8]
row = table[0].todense()
print type(row)
print row.shape

print "Closing HDF5 file...",
biom_f.close()
print "Done"
