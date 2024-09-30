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
#letters = "ab" # bcdefgh"
#print(letters)
#sys.exit(0)

testx = []

nlut = s2snp.S2sNp(200, 8)

def callb(letter, dims, datax):
    #print("callb", letter, dims, len(datax), "bytes")
    #scale to uniform
    #fff = fff.resize((sss[0], sss[1]))
    #fff = fff.resize((aaa, bbb))
    nlut.memorize2d(datax, letter, dims)

if __name__ == '__main__':

    #print("Train fonts")

    bw = s2sutil.load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    #print("bw size", bw.size)
    ppp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new("L", (500,300), color=(150) )

    aaa, bbb, row = s2sutil.trainfonts(letters, callb, sumx)
    #print("train ret", aaa, bbb, row)
    #nlut.dump()
    #sumx2 = Image.new("L", (500,300), color=(150) )
    #nlut.images(sumx2)
    #sumx2.show()
    #sys.exit()

    # Scan OK?
    ddd = bytes(bw.getdata())
    dddd = bytearray([200  for aa in range(len(ddd))])
    for yy in range(bw.size[1]):
        rowx = yy * bw.size[0]
        for xx in range(bw.size[0]):
            #pp.putpixel((xx, yy), bw.getpixel((xx, yy) // 2)
            dddd[rowx + xx] = ddd[rowx + xx] // 2
    pp = Image.frombuffer("L", bw.size, dddd)
    #pp = Image.frombuffer("L", bw.size, ddd)

    # Recog. For every coordinate, run recog
    for yy in range(0, bw.size[1], 1):
        rowxx = yy * bw.size[0]
        for xx in range(0, bw.size[0], 1):
            # Test where the presumptive 'a'  is
            if xx == 34 and yy == 15:
                ddddd = bytearray([220  for aa in range(len(ddd))])
                #arrx = []
                for yyy in range(yy, yy + bbb, 1):
                    if yyy >= bw.size[1]:
                        continue
                    for xxx in range(xx, xx + aaa, 1):
                        if xxx >= bw.size[0]:
                            continue
                        pix = bw.getpixel((xxx, yyy))
                        #ppp.putpixel((xxx, yyy), pix // 2)
                        #ddddd[(yyy-yy) * aaa + (xxx-xx)] = pix

                nlut.recall2d(rowxx + xx, bw.size, list(bw.getdata()))
                #ppp = Image.frombuffer("L", (aaa, bbb), ddddd)


    # Show
    sumx.paste(bw,  (10, row+40,))
    sumx.paste(pp,  (10, row+100,))
    sumx.paste(ppp, (pp.size[0] + 20, row+100,))

    #sumx.show()

    sumx3 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx3.show()

# EOF
