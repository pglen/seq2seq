#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, random, math

from PIL import Image, ImageFont, ImageDraw

import s2sutil
import s2snp

verbose = 0
imgdir = "png"

letters = [ chr(nn) for nn in range(32, 127) ]
#letters = "a" # bcdefgh"
#print(letters)

testx = []

nlut = s2snp.S2sNp(200, 8)

def callb(letter, dims, datax):
    #print("callb", letter, dims, len(datax), "bytes")
    #scale to uniform
    #fff = fff.resize((sss[0], sss[1]))
    #fff = fff.resize((aaa, bbb))
    nlut.memorize(datax, letter, dims)

if __name__ == '__main__':

    #print("Train fonts")

    bw = s2sutil.load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    #print("bw size", bw.size)

    orgx = bytes(bw.getdata())
    #print(orgx[1000:1500])
    #sys.exit(0)

    pp = Image.new(bw.mode, bw.size, color=255)
    ppp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new("L", (500,300), color=(150) )

    aaa, bbb, row = s2sutil.trainfonts(letters, callb, sumx)
    #print("train ret", aaa, bbb, row)
    #nlut.dump()
    sumx2 = Image.new("L", (500,300), color=(150) )
    nlut.images(sumx2)
    sumx2.show()

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
            #if len(ins) == aaa*bbb:
            #    res = nlut.recall(ins)
            #    pass
            #else:
            #    print("bad len", len(ins))

            #print("one cycle: %.3f ms" % ((time.time()-ttt) * 1000) )
            #if  nlut.distance != 10149:
            #    print("coor %2d %2d" % (xx, yy), "res:", nlut.outputs, "dist", nlut.distance)

    # Show                                (
    sumx.paste(bw,  (10, row+40,))
    sumx.paste(pp,  (10, row+100,))
    sumx.paste(ppp, (pp.size[0] + 20, row+100,))

    #sumx.show()

    sumx3 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx3.show()

# EOF
