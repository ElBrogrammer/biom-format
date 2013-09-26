#!/usr/bin/env bash
for table in tests/bench/tables/*.biom.gz
do
  unzipped_table=$(echo ${table} | sed 's/.gz//')
  gunzip -c ${table} > ${unzipped_table}
  hdf5_table=$(echo ${unzipped_table} | sed 's/.biom/.h5/')
  python biom2hdf5 ${unzipped_table} ${hdf5_table} sparse
done
