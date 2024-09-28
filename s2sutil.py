#!/usr/bin/env python

import os, sys, random, time

from PIL import Image, ImageFont, ImageDraw

from pgdict import *

# ------------------------------------------------------------------------

def pn(num, prec = 2):
    ''' print with specified precision '''
    return f"%-7.{prec}f" % num

def randmemb(var):

    ''' Deliver a random member of an array '''

    if type(var) != type( () ) and type(var) != type([]) :
        raise ValueError("Must be a list / array")

    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

def s2srand():
    ''' Deliver a random number in range of 0 to +1 '''
    ret = random.random();
    #print "%+0.3f " % ret,
    return ret

def sqr(vvv):
    return vvv * vvv

def parr(arr):
    ''' just print it '''
    for aa in arr:
        print(pn(aa), end = " ")
    print()

def load_font_img(fname):

    ''' load image to memory '''

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
    # Convert
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

    ''' Low pass filter. Peeks stay in place. '''

    lll = list(arrx)
    lenx = len(lll)
    for _ in range(factorx):
        # first and last unchanged
        for ddd in range(1, lenx-1):
            avg = lll[ddd-1] + lll[ddd] + lll[ddd+1]
            lll[ddd] = avg // 3
    return lll

def falledges(arrx):

    ''' detect falling edges '''

    lenx = len(arrx)
    prev = 0; fall = 0
    eee = [False for _ in range(lenx) ]
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

    ''' Detect rising edges '''

    lenx = len(arrx); prev = 0
    eee = [ False for _ in range(lenx) ]
    for ddd in range(lenx):
        #print(arrx[ddd], end = " " )
        if arrx[ddd] > prev:
            raisex = True
            eee[ddd] = True
        else:
            raisex = False
        prev = arrx[ddd]
        #print (eee[ddd])
    return eee

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

def measure_speed(func):

    ''' Decorator for speed measure '''

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
    # Special cases: leftover or all the same values
    if cntx  > 1:
        arr2.append((cntx-1, prev))
    return arr2

def trainfonts(letters, callb, sumx = None):

    ''' add fonts, callback with font and dim and array '''

    #font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    sfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 6)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    # Flatten font to linear, calc dims
    row = 10; hhh = 10
    aaa = 0; bbb = 0
    for aa in letters:
        sss = font.getsize(aa)
        aaa += sss[0]; bbb += sss[1]
    aaa //= len(letters)
    bbb //= len(letters)

    for aa in letters:
        sss = font.getsize(aa)
        fw = "%s" % (sss[0]); fh = "%s" % (sss[1])
        fww = sfont.getsize(fw)
        fhh = sfont.getsize(fh)

        annox = Image.new("L", fww, color=(200) )
        draw = ImageDraw.Draw(annox)
        draw.text((0, 0), fw, font=sfont)

        annoy = Image.new("L", fhh, color=(200) )
        draw = ImageDraw.Draw(annoy)
        draw.text((0, 0), fh, font=sfont)

        fff = Image.new("L", sss, color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)

        # Scan for empty rows
        if aa != " ":
            fff2 = cropx(cropy(fff))
        else:
            fff2 = fff

        ddd = fff2.getdata()
        callb(aa, fff2.size, ddd)

        if sumx:
            sumx.paste(fff2, (hhh, row,))
            sumx.paste(annox, (hhh, row - 6,))
            sumx.paste(annoy, (hhh, row + fff2.size[1] + 1,))

        hhh += sss[0] + 6
        if hhh > 450:
            hhh = 10
            row += bbb + 16
        #nlut.dump()

    return aaa, bbb, row


def cropx(fff):

    ''' trim left and right '''

    sss = fff.size
    payl = 0; skip = 0; endskip = sss[0]
    for yyy in range(sss[0]):
        rowx = sss[1] * yyy
        full = 1
        for xxx in range(sss[1]):
            ccc = fff.getpixel((yyy, xxx,))
            if ccc != 255:
                full = 0
                payl = 1
        if full:
            if not payl:
                skip += 1
            else:
                endskip -= 1
        #print("skip", skip)
        #skip = 0
    fff2 = fff.crop((skip, 0, endskip, sss[1]))
    return fff2

def cropy(fff):

    ''' trim top and buttom '''

    sss = fff.size
    payl = 0; skip = 0; endskip = sss[1]
    for yyy in range(sss[1]):
                rowx = sss[0] * yyy
                full = 1
                for xxx in range(sss[0]):
                    ccc = fff.getpixel((xxx, yyy,))
                    if ccc != 255:
                        full = 0
                        payl = 1
                if full:
                    if not payl:
                        skip += 1
                    else:
                        endskip -= 1
        #print("skip", skip)
        #skip = 0
    fff2 = fff.crop((0, skip, sss[0], endskip))
    return fff2

def scalex(mode, orgdim, newdim, datax):

    ''' Scale image data '''

    print("scalex", mode, orgdim, newdim, )
    aspx =  orgdim[0] / newdim[0]
    aspy =  orgdim[1] / newdim[1]
    #print("sp", aspx, aspy)
    ret = bytearray(newdim[0] * newdim[1])
    for aa in range(newdim[1]):
        offs =  aa * newdim[0]
        aaa = int(aa * aspy)
        offs2 =  aaa * orgdim[0]
        for bb in range(newdim[0]):
            bbb = int(bb * aspx)
            ret[offs + bb] = datax[offs2 + bbb]

    return bytes(ret)

#@measure_speed
def mirror(mode, dims, lettx):

    ''' Mirror array '''
    retx = bytearray(dims[0] * dims[1])
    for aa in range(dims[1]):
        offs = dims[0] * aa
        for bb in range(dims[0]):
            retx[offs + ((dims[0]-1) - bb)] = lettx[int(bb + offs)]
    return bytes(retx)

def vmirror(mode, dims, lettx):

    ''' Vertical mirror array '''

    retx = bytearray(dims[0] * dims[1])
    for aa in range(dims[1]):
        offs = dims[0] * aa
        offs2 = dims[0] * ((dims[1] - 1) - aa)
        for bb in range(dims[0]):
            retx[offs + bb] = lettx[bb + offs2]
    return bytes(retx)

def swapxy(mode, dims, lettx):

    ''' Swap x axis with y axis '''

    retx = bytearray(dims[0] * dims[1])
    for aa in range(dims[1]):
        offs = dims[0] * aa
        for bb in range(dims[0]):
            offs2 = dims[1] * bb
            retx[offs2 + aa] = lettx[offs + bb]
    return bytes(retx)

def blur(mode, dims, fact, lettx):

    ''' Blur image array '''

    retx = bytearray(dims[0] * dims[1])
    for aa in range(dims[1]):
        offs = dims[0] * aa
        linex = bytearray(lettx[offs:offs+dims[0]])
        linex = lowpass(linex, fact)
        for bb in range(dims[0]):
            pass
            retx[offs + bb] = linex[bb]
    return bytes(retx)

def vblur(mode, dims, fact, lettx):

    ''' Blur image array, vertically '''

    retx = bytearray(dims[0] * dims[1])
    for aa in range(dims[0]):
        linex = bytearray(dims[1])
        for bb in range(dims[1]):
            offs = dims[0] * bb
            linex[bb] = lettx[offs + aa]
        linex = lowpass(linex, fact)
        for bb in range(dims[1]):
            offs = dims[0] * bb
            retx[offs + aa] =  linex[bb]
    return bytes(retx)

if __name__ == '__main__':

    #print("Testing utils")
    #print(pn(1/3))

    import argparse
    parser = argparse.ArgumentParser(
                        prog='s2util',
                        description='s2util tests',
                        epilog='')

    parser.add_argument('-s', '--scale', default=0, action="store_true",
                                    help="Test scale image")
    parser.add_argument('-m', '--mirror', default=0, action="store_true",
                                    help="Test mirror image")
    parser.add_argument('-v', '--vmirror', default=0, action="store_true",
                                    help="Test vertical mirror image")
    parser.add_argument('-w', '--swap', default=0, action="store_true",
                                    help="Test swap x y on image")
    parser.add_argument('-b', '--blur', default=0, action="store_true",
                                    help="Test blur image")
    parser.add_argument('-B', '--vblur', default=0, action="store_true",
                                    help="Test vertical blur image")
    parser.add_argument('-x', '--crossblur', default=0, action="store_true",
                                    help="Test cross blur image")
    parser.add_argument('-t', '--fact', default=1, type=int, action="store",
                                    help="Blur factor")
    args = parser.parse_args()
    #print("args", args)

    if args.scale:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw,  (10, 10,))
        orgx = bytes(bw.getdata())
        fact = 4
        newsize = (int(bw.size[0] * fact), int(bw.size[1] * fact))
        orgx2 = scalex("L", bw.size, newsize, orgx)
        bw2 = Image.frombytes("L", newsize, orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()

    elif args.mirror:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        fact = 4
        orgx2 = mirror("L", bw.size, orgx)
        bw2 = Image.frombytes("L", bw.size, orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()
    elif args.vmirror:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        fact = 4
        orgx2 = vmirror("L", bw.size, orgx)
        bw2 = Image.frombytes("L", bw.size, orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()
    elif args.swap:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        fact = 4
        orgx2 = swapxy("L", bw.size, orgx)
        bw2 = Image.frombytes("L", (bw.size[1], bw.size[0]), orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()

    elif args.blur:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        orgx2 = blur("L", bw.size, args.fact, orgx)
        bw2 = Image.frombytes("L", (bw.size[0], bw.size[1]), orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()

    elif args.vblur:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        orgx2 = vblur("L", bw.size, args.fact, orgx)
        bw2 = Image.frombytes("L", (bw.size[0], bw.size[1]), orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()

    elif args.crossblur:
        bw = load_bw_image(os.path.join("png", "srect_white_abc.png"))
        sumx = Image.new("L", (500,300), color=(150) )
        sumx.paste(bw, (10, 10,))
        orgx = bytes(bw.getdata())
        orgx1 = vblur("L", bw.size, args.fact, orgx)
        orgx2 = blur("L", bw.size, args.fact, orgx1)
        #orgx3 = vblur("L", bw.size, args.fact, orgx2)
        bw2 = Image.frombytes("L", (bw.size[0], bw.size[1]), orgx2)
        sumx.paste(bw2,  (10, 70,))
        sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
        sumx2.show()

    else:
        #print("Use: s2util --help")
        print(parser.print_help())
# EOF
