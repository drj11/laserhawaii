#!/usr/bin/env python

import sys

import arc

def main(out=sys.stdout):
    raster = arc.Raster()
    # number of tiles in X and Y
    tx,ty = raster.header.tiletiles
    # size of each tiles in pixels
    tw,th = raster.header.tilesize
    w = tx*tw
    h = ty*th
    out.write("P2 %d %d 1\n" % (w, h))

    for row in raster.rows():
      b = (int(x >= 0) for x in row)
      out.write("%s\n" % ' '.join(str(x) for x in b))

if __name__ == '__main__':
   main()
