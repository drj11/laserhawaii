import os
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

    toPNM(mode=mode, mask=open('hawaii_mask.pgm', 'w'), opt=opt)

def toPNM(out=sys.stdout, mask=open('/dev/null'),
  mode='height', opt={}):
    """Write (plain) PGM file out. Heights are truncated to
    integer values. A mask (PGM) is written to mask: any cell
    with NaN or negative height is written as 0 to the mask (1
    otherwise).
    """

    os.chdir('hawaii_dem')
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
    mask.write("P2 %d %d 1\n" % (w, h))

    for row in raster.rows():
      row = list(row)
      m = [int(x >= 0) for x in row]
      v = (int(x) if m else 0 for x,m in zip(row, m))
      out.write("%s\n" % ' '.join(str(x) for x in v))
      mask.write("%s\n" % ' '.join(str(x) for x in m))

if __name__ == '__main__':
   main()
