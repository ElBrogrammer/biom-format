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
data_grp = biom_f['data']
table = coo_matrix((data_grp['values'].value,
                    (data_grp['rows'].value, data_grp['columns'].value)),
                    shape=biom_f.attrs['shape'])
table = table.tocsr()
print "Done"

print "Closing HDF5 file...",
biom_f.close()
print "Done"
