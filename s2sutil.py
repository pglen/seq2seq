#!/usr/bin/env python

import sys, random, time

from PIL import Image

from s2sdict import *

def pn(num):
    return "% -7.3f" % num

# ------------------------------------------------------------------------

# Deliver a random member of an array

def randmemb(var):
    if type(var) != type( () ) and type(var) != type([]) :
        raise ValueError("Must be a list / array")
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

# ------------------------------------------------------------------------
# Deliver a random number in range of 0 to +1

def neurand():
    ret = random.random();
    #print "%+0.3f " % ret,
    return ret

def neurand2():
    ret = random.random() * 2 - 1;
    #print("neurand %+0.3f " % ret)
    return ret

def sqr(vvv):
    return vvv * vvv

def parr(arr):
    for aa in arr:
        print(pn(aa), end = " ")

    print()

def is_ok(val, ref):
    if val == ref:
        ret = "\033[32;1mOK\033[0m"
    else:
        ret = "\033[31;1mERR\033[0m"
    return ret

def newarr(size, fill):
    arrx = []
    for ee in range(size):
        arrx.append(fill)
    return arrx

def load_font_img(fname):

    arr = []; arr2 = []
    aaa = Image.open(fname)
    #print(aaa.format, aaa.size, aaa.mode, aaa.getbands())
    mmm = aaa.size[0]; eee = 0
    for aa in range(aaa.size[1]):
        mark = 0
        for bb in range(aaa.size[0]):
            xxx = aaa.getpixel((bb, aa,))
            #print (xxx, end=" ")

            if xxx != (255, 255, 255, 255):
                mark = 1
        if not mark:
            for bb in range(aaa.size[0]):
                #aaa.putpixel((bb, aa,), ( 255, 0, 255))
                pass
        else:
            begx = 0; endx = 0
            for bb in range(aaa.size[0]):
                xxx = aaa.getpixel((bb, aa,))
                if xxx != (255, 255, 255, 255):
                    begx = bb
                    break

            for bb in range(aaa.size[0]-1, -1, -1):
                xxx = aaa.getpixel((bb, aa,))
                if xxx != (255, 255, 255, 255):
                    endx = bb
                    break
                #aaa.putpixel((bb, aa,), ( 255, 255, 122))

            mmm = min(mmm, begx)
            eee = max(eee, endx)
            arr2. append(aa)
            #print(bb, begx, endx)

    for aa in arr2:
        for zz in range(mmm, eee):
            pix = aaa.getpixel((zz, aa,))
            if pix ==  (255, 255, 255, 255):
                pix = 255
            else:
                pix = 0
            arr.append(pix)

    #print(arr)
    #print(fname, eee-mmm, "x", len(arr2))
    #print("new", "L", eee-mmm, len(arr2), "data len", len(arr))

    ccc = Image.new("L", (eee-mmm, len(arr2)))
    ccc.putdata(arr)
    #ccc.show()

    #nsize = (eee-mmm) * len(arr2)

    return ccc


def load_bw_image(fname):

    im = Image.open(fname)
    #print(im.format, im.size, im.mode, im.getbands())

    arr3 = []
    for aa in range(im.size[1]):
        for bb in range(im.size[0]):
            pix = im.getpixel((bb, aa,))
            #print(pix)
            if pix ==  (255, 255, 255, 255):
                pix = 255
            else:
                pix = 0

            arr3.append(pix)

    bw = Image.new("L", im.size, color=(255) )
    bw.putdata(arr3)

    return bw

def lowpass(arrx, factorx = 1):

    ''' low pass filter '''

    lll = arrx[:]
    lenx = len(lll)
    for _ in range(factorx):
        # first and last unchanged
        for ddd in range(1, lenx-2):
            avg = lll[ddd-1] + lll[ddd] + lll[ddd+1]
            lll[ddd] = avg // 3
    return lll

def falledges(arrx):

    ''' detect falling edges '''

    lenx = len(arrx)
    prev = 0; fall = 0
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if arrx[ddd] < prev:
            if not fall:
                fall = True
                eee[max(0, ddd-1)] = True
        else:
            fall = False
        prev = arrx[ddd]
    return eee

def raisededges(arrx):

    ''' detect falling edges '''

    lenx = len(arrx)
    prev = 0; fall = 0
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if arrx[ddd] > prev:
            if not fall:
                fall = True
                eee[max(0, ddd-1)] = True
        else:
            fall = False
        prev = arrx[ddd]
    return eee

def plotvals(arrx, plotx, lab = ""):
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


def sections(thh1x, thh2y, bww, ppp = None):

    ''' Boundary by non zero sectons

          Parameters:
                    thh1x (arr):    zero crossings x dim
                    thh2y (arr):    zero crossings y dim
                    bww (Image):    image for debug output
                    ppp (Image):    image for debug output

            Returns:
                    DeepDict array of renderable

    '''

    ret = DeepDict()

    prog = 0; xlen = len(thh2y); curr = 0
    while True:
        if prog >=  xlen:
            break
        if thh2y[prog]:
            while True:
                if prog >=  xlen:
                    break
                if  not thh2y[prog]:
                    #print()
                    break
                # one X section
                _sectiony(thh1x, prog, curr, ret, bww, ppp)
                prog += 1
            curr += 1
            #break
        prog += 1
    #for aa in ret:
    #    for bb in ret[aa]:
    #        #print(aa, bb)
    #        for cc in ret[aa][bb]:
    #            #print(aa, bb, cc) #ret[aa][bb][cc])
    #            for dd in ret[aa][bb][cc]:
    #                print("[%d, %d, %d, %d] %d" % (aa,bb,cc,dd, ret[aa][bb][cc][dd]) )
    #def callme(keys, val):
    #    print(keys, val)
    #ret.recurse(callb = callme)
    #print(ret)
    return ret

def _sectiony(arry, xx, currx, ret, bww, ppp):
    progy = 0; leny = len(arry);  curry = 0;
    while True:
        if progy >= leny:
            break
        if arry[progy]:
            while(True):
                if not arry[progy]:
                    break
                #bww.putpixel((0, progy),  200)
                col = bww.getpixel((xx, progy))
                if ppp:
                    ppp.putpixel((xx, progy), 200 - col)
                ret.setdeep((currx,curry,xx,progy), col)
                #ret[currx,curry,xx,progy] = col
                #print(currx,curry,xx,progy, col)
                progy += 1
            #print("[", xx, prog, end = " ] " )
            curry += 1
            #break
        progy += 1

# Decorator for speed measure
def measure(func):
    def run(*args, **kwargs):
        ttt = time.time()
        ret = func(*args, **kwargs)
        print("Exe: %.3f us" % ((time.time() - ttt) * 1000000))
        return ret
    return run

def rle(arr):

    ''' run length encoding '''

    arr2 = []; cntx = 1
    if not len(arr):
        return arr2

    prev = arr[0];
    for bb in arr:
        if prev != bb:
            if cntx == 1:
                arr2.append(prev)
            else:
                arr2.append((cntx, prev))
            prev = bb
            cntx = 1
        else:
            cntx += 1

    # Special case: all the same values
    if cntx  > 1:
        arr2.append((cntx-1, prev))

    return arr2


def scale(lettx, newx, newy, ppp = None):

    rows = [] ; cols = []

    #print(lettx)

    for nx, ny, val in lettx:
        if nx not in cols:
            cols.append(nx)
        if ny not in rows:
            rows.append(ny)
    aspx =  newx /len(cols)   ; aspy =   newy / len(rows)
    #print("aspx %.3f" % aspx, "aspy %.3f" % aspy, "new:",
    #                newx, "old", len(cols), newy, len(rows))
    #ret = []
    retx = ret = DeepDict()
    for aa in range(newx):
        offs = len(rows) * aa
        for bb in range(newy):
            try:
                bbb = bb / aspx
                aaa = aa / aspy
                #print("%.3f " % aaa, "%.3f " %bbb, int(aaa), int(bbb))
                val = lettx[int(bbb + offs)] [2]
            except IndexError:
                #print(bbb, aaa, sys.exc_info())
                pass
            except:
                print(sys.exc_info())
            #ret.append((aa, bb, val))
            retx[aa][bb] = val

    if ppp:
        pass
        #for aa, bb, val in ret:
        #    ppp.putpixel((aa, bb), val)
        #    pass
    #print(len(ret))
    return ret

from PIL import Image, ImageFont, ImageDraw

def trainfonts(letters, nlut, sumx):

    #nlut = neulut.NeuLut(200, 8)

    #font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    # Flatten font to linear
    row = 10; hhh = 10
    aaa = 0; bbb = 0
    for aa in letters:
        sss = font.getsize(aa)
        aaa += sss[0]; bbb += sss[1]
    aaa //= len(letters)
    bbb //= len(letters)

    for aa in letters:
        sss = font.getsize(aa)
        fff = Image.new("L", sss, color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)
        #scale to uniform
        #fff = fff.resize((sss[0], sss[1]))
        fff = fff.resize((aaa, bbb))

        ddd = list(fff.getdata())
        if aa == 'a':
            testx = ddd[:]
        #print(aa, len(ddd), sss, ddd)
        nlut.memorize(ddd, aa)
        sumx.paste(fff, (hhh, row,))
        hhh += aaa + 5
        if hhh > 450:
            hhh = 10
            row += 20
        #nlut.dump()

    return aaa, bbb, row

# EOF
