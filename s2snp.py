#!/usr/bin/env python3

# ------------------------------------------------------------------------
# Neural network test

'''
   Test cases for simple gates with diverging values
'''

import random, math, sys, argparse, time, uuid
import numpy as np

from PIL import Image, ImageFont, ImageDraw

import pgutil
import s2sutil

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------

class S2sNp():

    ''' The basic building block, numpy implementation
            The training material is pushed to an array;
            The lookup is executed finding the closest match
    '''

    def __init__(self, inputs, outputs):

        global gl_serial

        self.serial = gl_serial; gl_serial += 1;
        self.verbose = 0
        #if VERBOSE:
        #    print("neulut init ",  "inuts %.03f " % inputs) #, end=' ')
        self.uuid = uuid.uuid1()
        #print(self.uuid)
        self.inputs  = np.zeros(inputs)
        self.outputs  = np.zeros(outputs)
        self.distance = 0
        self.trarr = []

    # These are helpers

    def inlen(self):
        return len(self.inputs)

    def outlen(self):
        return len(self.outputs)

    # --------------------------------------------------------------------
    # Compare arrays, return closest match value

    def _cmp(self, ins, val):

        #print("_cmp", len(ins), len(val))
        #ret = np.power(np.subtract(ins, val),2)
        ret = np.abs(np.subtract(ins, val))
        #print("ins", ins, "val", val, "ret",
        #           ret, "sum", ret.sum())
        sum = ret.sum()
        #print("_cmp", ins, val, sum)
        return sum

    # --------------------------------------------------------------------
    def recall(self, ins):

        '''
            Evaluate one neuron. Find the smallest diff.
        '''

        if self.verbose > 1:
            print("recall", "len", len(ins), "ins", ins)

        old = 0xffffffff ; outx = []
        for aa in self.trarr:
            ss = self._cmp(ins, aa[0])
            if self.verbose > 2:
                slx = s2sutil.rle(aa[0])[:8]
                print("recall:",  aa[1], "cmp", ss, "data", slx, end = "\n")
            if old > ss:
                old = ss
                outx = aa[1]

        self.outputs = outx
        self.distance = old

        if self.verbose > 0:
            print("outx", outx, "dist", "%.2f" % self.distance)
        return outx

    def recall2d(self, offs, dimx, imgdat):

        '''
            Evaluate one neuron. Find the smallest diff.
        '''

        #print("recall2d", "offs:", offs, "dimx:", dimx)
        #print("data", s2sutil.rle(imgdat)[:6])

        for bb in range(12):
            rowx = bb * dimx[0]
            curr = imgdat[offs + rowx : offs + rowx + 10]
            for cc in curr:
                if cc > 128:
                    print(" ", end = "")
                else:
                    print("*", end = "")
            print()
        print()

        old = 0xfffffff ; outx = ''
        for aa in self.trarr:

            #if aa[1] != "8":
            #    continue

            for bb in range(aa[2][1]):
                #    print(aa[0][bb])
                for cc in aa[0][bb]:
                    if cc > 128:
                        print(" ", end = "")
                    else:
                        print("*", end = "")
                print()

            print("char '%c'" % aa[1], aa[2], end = " ")
            #for bb in range(aa[2][1]):
            #    print(aa[2], type(aa[0][bb]), aa[0][bb])

            ss = 0
            for bb in range(aa[2][1]):
                rowx = bb * dimx[0]
                curr = imgdat[offs + rowx : offs + rowx + aa[2][0]]
                #print("curr", type(curr), curr)
                curr2 = np.array(curr, dtype="ubyte")
                #print("curr2", type(curr2), curr2)
                ss += self._cmp(curr2, aa[0][bb])
                #print("%.2f" % ss, end = " ")

            #ss /= aa[2][0] * aa[2][1]

            if old > ss:
                old = ss
                outx = aa[1]

            print("old=%.2f" % old)
            '''if 1: #VERBOSE > 1:
                    slx = s2sutil.rle(img[bb])
                    print("recall2d:",  aa[1], ss, slx, end = "\n")
                '''
        self.outputs = outx
        self.distance = old
        if 1: #VERBOSE > 1:
            print("outx", outx, "%.2f" % old)
        return outx

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):

        ''' Show details. For testing '''

        for cnt, aa in enumerate(self.trarr):
            #print(aa[0][:16])
            arr2 = s2sutil.rle(aa[0])
            print("lett", "'" + aa[1] + "'", "dims", aa[2], arr2[:8], "...")

    def memorize(self, ins, outs, dims = (), step = 0):

        ''' Remember training material '''

        if self.verbose > 2:
            print("memorize", "in:", ins, outs)
        arrx = np.array(ins)
        if self.verbose > 1:
            print("memorize", "len:", len(arrx), "ins:", arrx, "outs:", outs)
        self.trarr.append((arrx, outs, dims, step))

    def memorize2d(self, ins, outs, dims = (), step = 1):

        ''' Remember training material for 2d data '''

        if self.verbose > 1:
            print("train", (cnt * 20, 0), rle(ins)[:8])
        #if outs != 'a':
        #    return
        arrx = np.array(ins, dtype="ubyte")
        arrx = arrx.reshape((dims[1], dims[0]))
        #arrx = arrx.reshape((dims[0], dims[1]))

        #print("arrx", arrx.shape)
        #print(arrx)
        self.trarr.append((arrx, outs, dims, step))

    def images(self, sumx):

        ''' Put images to surface. For testing '''

        xx = 10; yy = 10
        for cnt, aa in enumerate(self.trarr):
            try:
                #print("np", aa[0].shape, aa[0].size)
                #iii = Image.frombuffer("L", aa[2], aa[0] )
                #iii = Image.frombytes("L", aa[2], aa[0] )
                #arrx = aa[0].reshape((aa[2][1], aa[2][0]))
                #print("arrx", arrx.shape, arrx.size)
                iii = Image.fromarray(aa[0], mode="L")
                xx += aa[2][0] + 2
                if xx > 480:
                    xx = 10
                    yy += aa[2][1] + 2
                sumx.paste(iii, (xx, yy))

            except:
                print("exc:", aa[1], sys.exc_info())
                #raise
        return xx, yy

# ------------------------------------------------------------------------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog='neunp',
                    description='S2S (sequence to sequence) neural numpy demo of OR and AND gate logic',
                    epilog='')
    parser.add_argument('-c', '--count',
                    help = "Number of gate inputs added", default=0, type=int)
    parser.add_argument('-t', '--time', default=0, action="store_true",
                    help = "Show timing of the operations")
    parser.add_argument('-v', '--verbose', default=0, action="count",
                    help = "Show more info. Add -vv.. for more detail.")

    #global args
    args = parser.parse_args()

    VAL  = 0.5;   VAL2 = 0.6

    arr_0 =  (0,0)
    arr_1 =  (0,VAL)
    arr_2 =  (VAL,0)
    arr_3 =  (VAL,VAL)

    def testneu(nnn, tin, tout):
        tttt = 0
        for cnt, aa in enumerate(tin):
            ttt = time.time()
            nnn.recall(aa)
            tttt +=  time.time() - ttt
            print("in", aa[:12], "out",  nnn.outputs, pgutil.is_ok(nnn.outputs, tout[cnt]))
        if args.time:
            print("%.3f ms" % (tttt * 1000) )

    def test_train_check(in_arrx, ou_arrx,  tin_arrx, tou_arrx):

        in_arr = []; tin_arr = []
        # Padd with ins from comline
        for cnt, cc in enumerate(in_arrx):
            in_comp =  [0 for aa in range(args.count)]
            in_arr.append(list(cc) + in_comp)
            tin_arr.append(list(tin_arrx[cnt]) + in_comp)
        if args.verbose > 0:
            print("in_arr:", in_arr)
            #print("ou_arrx", ou_arrx)
        nn = S2sNp(len(in_arr), 1)
        nn.verbose = args.verbose
        for aa in range(len(in_arr)):
            nn.memorize(in_arr[aa], ou_arrx[aa])
        testneu(nn, tin_arr, tou_arrx)

    # imitate the AND gate
    in_andarr =  (arr_0,  arr_1,  arr_2,  arr_3,)
    ou_andarr =  (0, 0, 0, 1)
    tin_andarr =  ((0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_andarr =  (0, 0, 0, 1)

    print("NeuNp AND:")
    test_train_check(in_andarr, ou_andarr, tin_andarr, tou_andarr)

    # imitate the OR gate
    in_orarr =  (arr_0, arr_1,  arr_2,  arr_3, )
    ou_orarr =  (0, 1, 1, 1,)
    tin_orarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_orarr =  (0, 1, 1, 1,)

    print("NeuNp OR:")
    test_train_check(in_orarr, ou_orarr, tin_orarr, tou_orarr)

# EOF
