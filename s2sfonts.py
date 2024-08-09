#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, random, math

from PIL import Image, ImageFont, ImageDraw

from s2sutil import *

#import neulut
import s2snp

verbose = 0
imgdir = "png"

letters = [ chr(nn) for nn in range(32, 127) ]
letters = "abcdefgh"

#print(letters)

testx = []

if __name__ == '__main__':

    #print("Train fonts")

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    print("bw size", bw.size)

    orgx = bytes(bw.getdata())
    #print(orgx[1000:1500])
    #sys.exit(0)

    pp = Image.new(bw.mode, bw.size, color=255)
    ppp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new("L", (500,300), color=(150) )

    nlut = s2snp.S2sNp(200, 8)

    aaa, bbb, row = trainfonts(letters, nlut, sumx)

    # Recog. For every coordinate, build input
    for yy in range(0, bw.size[1] - bbb, 1):
        for xx in range(0, bw.size[0] - aaa, 1):
            ins2 = []
            for yyy in range(bbb):
                start = (yyy + yy) * bw.size[0] + xx;
                #print(orgx[start:start+aaa])
                ins2.append(orgx[start:start+aaa])
            ins = list(b"".join(ins2))
            #print(rle(ins))
            if xx == 30 and yy == 10:
                #print("ins2", ins2)
                for yyyy in range(bbb):
                    for xxxx in range(aaa):
                        try:
                            pix = bw.getpixel((xx + xxxx, yy + yyyy))
                            pp.putpixel((xxxx + xx, yyyy + yy), pix // 2)
                            ppp.putpixel((xxxx + xx, yyyy + yy), ins2[yyyy][xxxx])
                        except IndexError:
                            pass
                        except:
                            print(sys.exc_info())

            #ttt = time.time()
            if len(ins) == aaa*bbb:
                res = nlut.recall(ins)
                pass
            else:
                print("bad len", len(ins))

            #print("one cycle: %.3f ms" % ((time.time()-ttt) * 1000) )
            if  nlut.distance != 10149:
                print("coor %2d %2d" % (xx, yy), "res:", nlut.outputs, "dist", nlut.distance)

    # Show                                (
    sumx.paste(bw,  (10, row+40,))
    sumx.paste(pp,  (10, row+100,))
    sumx.paste(ppp, (10, row+160,))
    #sumx.show()

    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
