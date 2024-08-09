#!/usr/bin/env python3

# ------------------------------------------------------------------------
# Neural network test

'''
   Test cases for simple gates with diverging values
'''

import random, math, sys, argparse

from s2sutil import *
from pgutil import *

import numpy     as np

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------
# The basic building block, numpy implementation
# The training material is pushed to an array;
# The lookup is executed finding the closest match

class S2sNp():

    def __init__(self, inputs, outputs):

        global gl_serial

        # These are helpers
        self.serial = gl_serial; gl_serial += 1;
        if verbose:
            print("neulut init ",  "inuts %.03f " % inputs) #, end=' ')

        self.inputs  = np.zeros(inputs)
        self.outputs  = np.zeros(outputs)
        self.distance = 0
        self.trarr = []

    def inlen(self):
        return len(self.inputs)

    # --------------------------------------------------------------------
    # Compare arrays, return closest match value

    def cmp2(self, ins, val):
         #ret = np.power(np.subtract(ins, val),2)
         ret = np.abs(np.subtract(ins, val))
         #print("ins", ins, "val", val, "ret",
         #           ret, "sum", ret.sum())
         sum = ret.sum()
         #print("cmp2", ins, val, sum)
         return sum

    # --------------------------------------------------------------------
    # Fire one neuron. Find the smallest diff.

    def recall(self, ins, stride=1):
        #print("fire", ins[:12])
        old = 0xffff ; outx = []
        for aa in self.trarr:
            ss = self.cmp2(ins, aa[0])
            if verbose > 1:
                print("fire",  aa[1], ss, rle(aa[0])[:8], end = "\n")
            if old > ss:
                old = ss
                outx = aa[1]

        self.outputs = outx
        self.distance = old
        if verbose > 1:
            print("outx", outx)
        return outx

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):
        for cnt, aa in enumerate(self.trarr):
            #print(aa[0][:16])
            arr2 = rle(aa[0])
            print("dummp %-2d" % cnt, aa[1], arr2[:8], " ...")

    def memorize(self, ins, outs, step = 1):
        if verbose > 1:
            print("train", outs, rle(ins)[:8])
        self.trarr.append((np.array(ins), outs, step))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='neunp',
                        description='neural numpy demo',
                        epilog='')
    parser.add_argument('-c', '--count', default=2, type=int)
    parser.add_argument('-t', '--time', default=0, action="store_true")

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
            print("in", aa[:12], "out",  nnn.outputs, is_ok(nnn.outputs, tout[cnt]))
        if args.time:
            print("%.3f ms" % (tttt * 1000) )

    def test_train_check(in_arrx, ou_arrx,  tin_arrx, tou_arrx):

        in_arr = []; tin_arr = []
        for cnt, cc in enumerate(in_arrx):
            in_comp =  [0 for aa in range(args.count)]
            in_arr.append(list(cc) + in_comp)
            tin_arr.append(list(tin_arrx[cnt]) + in_comp)
        #print(in_arr)
        nn = S2sNp(len(in_arr), 1)
        for aa in range(len(in_arr)):
            nn.memorize(in_arr[aa], ou_arrx[aa])
        testneu(nn, tin_arr, tou_arrx)

    # imitate the AND gate
    in_andarr =  (arr_0, arr_1,  arr_2,  arr_3,)
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
