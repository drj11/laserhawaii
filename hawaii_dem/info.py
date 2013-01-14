#!/usr/bin/env python

# see http://home.gdal.org/projects/aigrid/aigrid_format.html

import struct

def bounds(filename='dblbnd.adf'):
    bytes = open(filename).read()
    bounds = struct.unpack('>4d', bytes)
    return bounds

print "bounds (*10e-4 degrees?)", bounds()

def adfIndex(filename='w001001x.adf'):
    """Returns a list of pairs."""
    bytes = open(filename).read()
    magic = bytes[0:8]
    exemplar = '0000270AFFFFFC14'.decode('hex')
    if magic != exemplar:
      raise BadMagic("magic %s exemplar %s" %
        (magic.encode('hex'), exemplar.encode('hex')))

    size, = struct.unpack('>l', bytes[24:28])

    l = []
    for i in range(100,size*2,8):
      pointer = struct.unpack('>2l', bytes[i:i+8])
      l.append(pointer)
    return l

index = adfIndex()
print index[:10]
