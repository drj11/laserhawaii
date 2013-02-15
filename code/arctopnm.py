#!/usr/bin/env python

import sys

import arc

def main(argv=None):
    import getopt
    if argv is None:
        argv = sys.argv

    opt, arg = getopt.getopt(argv[1:], '', ['band='])
    mode = 'height'
    for k,v in opt:
        if k == '--band':
            mode = 'band'
            opt = dict(band=float(v))

    toPNM(mode=mode, opt=opt)

def toPNM(out=sys.stdout, mode='height', opt={}):
    out = sys.stdout
    raster = arc.Raster()
    # number of tiles in X and Y
    tx,ty = raster.header.tiletiles
    # size of each tiles in pixels
    tw,th = raster.header.tilesize
    w = tx*tw
    h = ty*th
    # NB Truncate float 
    MAXVAL = 1 + int(raster.stats[1])
    out.write("P2 %d %d %d\n" % (w, h, MAXVAL))

    for row in raster.rows():
      v = (int(x) if x >= 0 else MAXVAL for x in row)
      out.write("%s\n" % ' '.join(str(x) for x in v))

if __name__ == '__main__':
   main()
