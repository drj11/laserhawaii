#!/usr/bin/env python
# Reads ARC GRID files.  aka ESRI Grid.

# see http://home.gdal.org/projects/aigrid/aigrid_format.html

import itertools
import operator
import struct
import sys

def bounds(filename='dblbnd.adf'):
    bytes = open(filename).read()
    bounds = struct.unpack('>4d', bytes)
    return bounds

# For the Hawaii DEM file the bound are in meters, referenced to
# some particular UTM coordinate system.

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

class Struct:
    def __init__(self, **k):
        self.__dict__.update(k)

    def __repr__(self):
        return "Struct(%r)" % self.__dict__

def adfHeader(filename='hdr.adf'):
    bytes = open(filename).read()
    magic = bytes[0:8]
    exemplar = 'GRID1.2\x00'
    if magic != exemplar:
      raise BadMagic("magic %s exemplar %s" %
        (magic.encode('hex'), exemplar.encode('hex')))
    celltype,compression = struct.unpack(">2l", bytes[16:24])
    pixelsize = struct.unpack(">2d", bytes[256:272])
    reference = struct.unpack(">2d", bytes[272:288])
    tiletiles = struct.unpack(">2l", bytes[288:296])
    w,dummy_,h = struct.unpack(">3l", bytes[296:308])
    return Struct(celltype=celltype, compression=compression,
      pixelsize=pixelsize, reference=reference,
      tiletiles=tiletiles, tilesize=(w,h))


class Raster:
    def __init__(self, header=adfHeader(), index=adfIndex(),
      filename="w001001.adf"):
        self.header = header
        self.index = index
        self.fd = open(filename, 'rb')
        self.celltype = self.header.celltype

    def tileRaw(self, i):
        pointer = self.index[i]
        o,s = pointer
        self.fd.seek(2*o)
        bytes = self.fd.read(2 + 2*s)
        if self.celltype == 2:
            res = struct.unpack(">%df" % (s//2), bytes[2:])
            return res
        return bytes

    def tile(self, i):
        """Return a sequence of sequences (a 2D "array" if you
        like)."""

        w,h = self.header.tilesize

        return list(grouper(w, self.tileRaw(i)))

    def tiles(self):
        """Yield each tile."""
        for i in range(operator.mul(*self.header.tiletiles)):
            yield self.tile(i)

    def rows(self):
        # Number of tile in each row
        nrowtiles = self.header.tiletiles[0]
        for tilerow in grouper(nrowtiles, self.tiles()):
            # tilerow is a single row of tiles.
            for pixelrow in zip(*tilerow):
                # pixel row is a single row of pixels, but
                # blocked up into nrowtiles chunks each of width
                # tilesize[0].
                yield list(itertools.chain(*pixelrow))

# http://docs.python.org/2/library/itertools.html#recipes
def grouper(n, i):
  args = [iter(i)]*n
  return itertools.izip(*args)

def main():
    print "bounds", bounds()
    print adfHeader()
    index = adfIndex()
    print index[:10]

if __name__ == '__main__':
    main()
