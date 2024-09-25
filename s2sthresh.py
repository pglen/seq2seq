#!/usr/bin/env python

# ------------------------------------------------------------------------
# Mark boundary of letters

'''
    Evaluate filled centers.

'''

import sys, random, math

from PIL import Image

import matplotlib
matplotlib.use('GTK3Cairo')
#matplotlib.use('Qt5Cairo')
import matplotlib.pyplot as plt

from s2sutil import *
from pgutil import *
from pgdict import *
import s2snp

LOWPASS = 0
imgdir = "png"

letters = [ chr(nn) for nn in range(32, 127) ]
letters = "abcdefgh"

cntx = 0
basex = []
letter = []

def plotvals(arrx, plotx, lab = ""):

    ''' Plot values for a one dim array '''

    xx = []; yy = []
    for cnt, aa in enumerate(arrx):
        xx.append(cnt); yy.append(aa)
    plotx.plot(xx, yy, label=lab)

def plotflags(fallx, arrx, plotx, nulval = 0, lab = ""):

    xxx = []; yyy = []
    for ccc in range(len(arrx)):
        if fallx[ccc]:
            flag = arrx[ccc]
            xxx.append(ccc); yyy.append(flag)
    plotx.scatter(xxx, yyy, label=lab)

def sections2(thh1x, thh2y, bww, ppp = None):

    ''' Boundary by non zero sectons

          Parameters:
                    thh1x (arr):    zero crossings x dim
                    thh2y (arr):    zero crossings y dim
                    bww (Image):    image for debug output
                    ppp (Image):    image for debug output

            Returns:
                    DeepDict array of renderable

    '''

def barearr(aaa, bbb, arrx):
    ret = []
    for yy in range(bbb):
        for xx in range(aaa):
            print(arrx[xx*yy])

    #for aa in arrx:
    #    #print(arrx[aa])
    #    ret.append(aa[2])

    return ret

def callme(keys, val):
    global cntx, basex, cols, rows
    if keys[0] == 0 and keys[1] == 0:
        if cntx == 0:
            basex = keys[2], keys[3]

        nx = keys[2]-basex[0];  ny = keys[3]-basex[1]
        #dd.putpixel((nx, ny), val)
        letter.append((nx, ny, val))

        print("%s %3d" % (keys, val),  end = "  ")
        if cntx % 3 == 2:
            print()
        cntx += 1

if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    dd = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new(bw.mode, (300, 200), color=240)

    arr = []
    for aa in range(0, bw.size[1], 1):
        sss = 0
        for bb in range(0, bw.size[0], 1):
            pxx = 255 - bw.getpixel((bb, aa))  # white is zero
            sss += pxx
        arr.append(sss)
    lll = lowpass(arr, LOWPASS)

    thh = []
    for cnt, aa in enumerate(lll):
        thh.append(aa > 10)
    #print(thh)

    arr2 = []
    for xx in range(0, bw.size[0], 1):
        ssss = 0
        for yy in range(0, bw.size[1], 1):
            pxx2 = 255 - bw.getpixel((xx, yy))  # white is zero
            ssss += pxx2
        arr2.append(ssss)
    lll2 = lowpass(arr2, LOWPASS)

    thh2 = []
    for cnt, aa in enumerate(lll2):
        thh2.append(aa > 10)
    #print(thh2)

    # Plot
    #plotvals(arr, plt, "Org")
    #plotvals(lll, plt, "LowPass")
    #plotflags(thh, thh, plt, -100, '1')
    #plt.xlabel("X Step"); plt.ylabel("Y Sums")
    #plt.legend()
    #plt.show()
    #sys.exit(0)
    '''
    global nlut
    nlut = s2snp.S2sNp(200, 8)
    aaa, bbb, row = trainfonts(letters, nlut, sumx)
    '''

    # Output it
    ret = sections(thh, thh2, bw, pp)
    print("ret", ret)

    #ret.recurse(callb = callme)
    print()

    '''
    # normalize
    sss = scalex(letter, letter.size, (10, 17), pp)
    #print(sss)
    bare = barearr(aaa, bbb, sss)
    print(bare)

    for aa in range(aaa):
        for bb in range(bbb):
             pass
             dd.putpixel((aa, bb), bare[aa + bb * aaa])
             #dd.putpixel((aa, bb), 100)

    res = nlut.fire(bare)
    print("res", res)
    '''

    sumx.paste(bw)
    sumx.paste(pp, (0, (bw.size[1] + 5) * 1))
    #sumx.paste(pp, ((bw.size[0] + 5), (bw.size[1] + 5) * 1))
    sumx.paste(dd, (0, (bw.size[1] + 5) * 2))
    #sumx.paste(dd, ((bw.size[0] + 5), (bw.size[1] + 5) * 2))

    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
