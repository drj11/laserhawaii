#!/usr/bin/env python

import sys

import arc

def main(out=sys.stdout):
    mode = 'height'
    raster = arc.Raster()
    # number of tiles in X and Y
    tx,ty = raster.header.tiletiles
    # size of each tiles in pixels
    tw,th = raster.header.tilesize
    w = tx*tw
    h = ty*th
    if mode == 'mask':
        MAXVAL = 1
    else:
        MAXVAL = 5000
    out.write("P2 %d %d %d\n" % (w, h, MAXVAL))

    for row in raster.rows():
      if mode == 'mask':
          v = (int(x >= 0) for x in row)
      else:
          v = (int(round(x)) if x >= 0 else MAXVAL for x in row)
      out.write("%s\n" % ' '.join(str(x) for x in v))

if __name__ == '__main__':
   main()
