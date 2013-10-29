#!/usr/bin/env python

from sys import argv
from gzip import open as gzip_open
from biom.parse import parse_biom_table

if __name__ == '__main__':
    table = parse_biom_table(gzip_open(argv[1]))
    
    md = dict([(obs_id, {'FOO': i % 8}) for i, obs_id in enumerate(table.ObservationIds)])
    table.addObservationMetadata(md)

    foo = table.binObservationsByMetadata(lambda x: x['FOO'])
