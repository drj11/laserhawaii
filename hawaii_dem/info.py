#!/usr/bin/env python

# see http://home.gdal.org/projects/aigrid/aigrid_format.html

import struct

bytes = open('dblbnd.adf').read()
bounds = struct.unpack('>4d', bytes)
print "bounds (*10e-4 degrees?)", bounds

bytes = open('w001001x.adf').read()
magic = bytes[0:8]
exemplar = '0000270AFFFFFC14'.decode('hex')
print "Magic", magic==exemplar
size, = struct.unpack('>l', bytes[24:28])
print "Size", size, "shorts"
for i in range(100,size*2,8):
  pointer = struct.unpack('>2l', bytes[i:i+8])
  print pointer
