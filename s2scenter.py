#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, random, math

from PIL import Image, ImageFont, ImageDraw

import s2sutil
import s2snp

verbose = 0
imgdir = "png"

#letters = [ chr(nn) for nn in range(33, 127) ]
letters = [ chr(nn) for nn in range(ord('a'), ord('z')) ]
#letters += [ chr(nn) for nn in range(ord('A'), ord('z')) ]
#letters += [ chr(nn) for nn in range(ord('0'), ord('9')) ]
#letters = "0" # bcdefgh"
#print(letters)
#sys.exit(0)

testx = []


# ------------------------------------------------------------------------

def callb2(letter, img):

    sumx.pastex(img)

    img4 = Image.new(bw.mode, img.size, color=220)

    # Make it 0 and ff
    for yy in range(img.size[1]):
            ss = 0; ee = 0
            for xx in range(img.size[0]):
                col = img.getpixel((xx, yy))
                if col < 128:
                    img.putpixel((xx, yy), 0)
                else:
                    img.putpixel((xx, yy), 255)

    # Determine mid points, y axis major
    img2 = Image.new(bw.mode, img.size, color=200)
    for yy in range(img.size[1]):
        ss = -1; ee = -1; was = 0
        cols = []
        for xx in range(img.size[0]):
            col = img.getpixel((xx, yy))
            #img.putpixel((xx, yy), col * 2)
            #print("%02x" % col, end = " ")
            if col == 0:
                if not was:
                    ss = xx;
                    ee = -1
                    was = True
            else:
                if was:
                    ee = xx
                    was = False
                    cols.append((ss, ee))
                    #break
        # incomlete segment
        if was and ee == -1:
            ee = xx
            cols.append((ss, ee))
        for sss, eee in cols:
            #print("sss eee", sss, eee)
            img2.putpixel( (((eee-sss)//2 + sss), yy), 0)
            img4.putpixel( (((eee-sss)//2 + sss), yy), 0)
        #print()
        #print("    ss ee", ss, ee)

    # Determine mid points vertical x axis major
    img3 = Image.new(bw.mode, img.size, color=220)

    for xx in range(img.size[0]):
        ss = -1; ee = -1; was = 0
        cols = []
        for yy in range(img.size[1]):
            col = img.getpixel((xx, yy))
            ##img.putpixel((xx, yy), col * 2)
            #print("%02x" % col, end = " ")
            if col == 0:
                if not was:
                    ss = yy
                    ee = -1
                    was = True
            else:
                if was:
                    ee = yy
                    was = False
                    cols.append((ss, ee))
                    #break
        # incomlete segment
        if was and ee == -1:
            ee = yy
            cols.append((ss, ee))

        for sss, eee in cols:
            #print("sss eee", sss, eee)
            img3.putpixel( (xx, ((eee-sss)//2 + sss)), 0)
            img4.putpixel( (xx, ((eee-sss)//2 + sss)), 0)
            pass

    # Determine mid points SECOND pass X
    img5 = s2sutil.SumImg.new(bw.mode, img.size, color=150)
    img7 = s2sutil.SumImg.new(bw.mode, img.size, color=150)
    for yy in range(img4.size[1]):
        ss = -1; ee = -1; was = 0
        cols = []
        for xx in range(img4.size[0]):
            col = img4.getpixel((xx, yy))
            #img5.putpixel((xx, yy), col )
            #print("%02x" % col, end = " ")
            if col == 0:
                if not was:
                    ss = xx
                    ee = -1
                    was = True
            else:
                if was:
                    ee = xx
                    was = False
                    cols.append((ss, ee))
                    #break
        # incomlete segment
        if was and ee == -1:
            ee = xx
            cols.append((ss, ee))
        for sss, eee in cols:
            #print("sss eee", sss, eee)
            img5.putpixel( (((eee-sss)//2 + sss), yy), 0)
            img7.putpixel( (((eee-sss)//2 + sss), yy), 0)

    # Determine mid points SECOND pass Y
    img6 = s2sutil.SumImg.new(bw.mode, img.size, color=150)
    for xx in range(img4.size[0]):
        ss = -1; ee = -1; was = 0
        cols = []
        for yy in range(img4.size[1]):
            col = img4.getpixel((xx, yy))
            #img6.putpixel((xx, yy), col )
            #print("%02x" % col, end = " ")
            if col == 0:
                if not was:
                    ss = yy
                    ee = -1
                    was = True
            else:
                if was:
                    ee = yy
                    was = False
                    cols.append((ss, ee))
                    #break
        # incomlete segment
        if was and ee == -1:
            ee = yy
            cols.append((ss, ee))
        for sss, eee in cols:
            #print("sss eee", sss, eee)
            img6.putpixel( (xx, ((eee-sss)//2 + sss)), 0)
            img7.putpixel( (xx, ((eee-sss)//2 + sss)), 0)
    # Verify
    pp.pastex(img)

    ppp.pastex(img2)
    ppp.pastex(img3)
    ppp.pastex(img4)
    ppp.pastex(img5)
    ppp.pastex(img6)
    ppp.pastex(img7)

    img6r = img6.mag(2)
    sumx.pastex(img6r) #, (10, 200))

if __name__ == '__main__':

    #print("Train fonts")

    bw = s2sutil.load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    #print("bw size", bw.size)
    sss = (bw.size[0] * 2, bw.size[1]*3)
    ppp = s2sutil.SumImg.new(bw.mode, sss, color=255)
    pp = s2sutil.SumImg.new(bw.mode,  sss, color=255)
    sumx = s2sutil.SumImg.new("L", (500,300), color=(150) )

    #picx = s2sutil.SumImg.new("L", (20,20), color=(250) )
    aaa, bbb, row = s2sutil.trainfonts(letters, callb2)
    #sumx.newrow(bw)

    # Show
    #sumx.pastex(bw)
    sumx.newrow(bw)
    sumx.pastex(pp)
    sumx.pastex(ppp)

    sumx3 = sumx.mag(4)
    sumx3.show()

# EOF
