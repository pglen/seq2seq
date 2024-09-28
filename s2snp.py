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

VERBOSE = 0

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

        # These are helpers
        self.serial = gl_serial; gl_serial += 1;
        if VERBOSE:
            print("neulut init ",  "inuts %.03f " % inputs) #, end=' ')

        self.uuid = uuid.uuid1()
        #print(self.uuid)
        self.inputs  = np.zeros(inputs)
        self.outputs  = np.zeros(outputs)
        self.distance = 0
        self.trarr = []

    def inlen(self):
        return len(self.inputs)

    def outlen(self):
        return len(self.outputs)

    # --------------------------------------------------------------------
    # Compare arrays, return closest match value

    def _cmp(self, ins, val):
         #ret = np.power(np.subtract(ins, val),2)
         ret = np.abs(np.subtract(ins, val))
         #print("ins", ins, "val", val, "ret",
         #           ret, "sum", ret.sum())
         sum = ret.sum()
         #print("_cmp", ins, val, sum)
         return sum

    # --------------------------------------------------------------------
    def recall(self, ins, stride=1):

        '''
            Evaluate one neuron. Find the smallest diff.
        '''

        #print("recall", ins[:12])
        old = 0xffff ; outx = []
        for aa in self.trarr:
            ss = self._cmp(ins, aa[0])
            if VERBOSE > 1:
                print("recall",  aa[1], ss, rle(aa[0])[:8], end = "\n")
            if old > ss:
                old = ss
                outx = aa[1]

        self.outputs = outx
        self.distance = old
        if VERBOSE > 1:
            print("outx", outx)
        return outx

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):

        ''' Show details. For testing '''

        for cnt, aa in enumerate(self.trarr):
            #print(aa[0][:16])
            arr2 = s2sutil.rle(aa[0])
            print("lett", "'" + aa[1] + "'", "dims", aa[2], arr2[:8], " ...")

    def memorize(self, ins, outs, dims = (), step = 1):

        ''' Remember training material '''

        if VERBOSE > 1:
            print("train", (cnt * 20, 0), rle(ins)[:8])
        self.trarr.append((np.array(ins, dtype="ubyte"), outs, dims, step))
        #self.trarr.append((ins, outs, dims, step))

    def images(self, sumx):

        ''' Put images to surface. For testing '''

        xx = 10; yy = 10
        for cnt, aa in enumerate(self.trarr):
            try:
                #print("np", aa[0].shape, aa[0].size)
                #iii = Image.frombuffer("L", aa[2], aa[0] )
                iii = Image.frombytes("L", aa[2], aa[0] )
                #arrx = aa[0].reshape((aa[2][1], aa[2][0]))
                #print("arrx", arrx.shape, arrx.size)
                #iii = Image.fromarray(arrx, mode="L")
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

VAL  = 0.5;   VAL2 = 0.6
arr_0 =  (0,0)
arr_1 =  (0,VAL)
arr_2 =  (VAL,0)
arr_3 =  (VAL,VAL)

def test_or():

    in_orarr =  (arr_0, arr_1,  arr_2,  arr_3, )
    ou_orarr =  (0, 1, 1, 1,)
    tin_orarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_orarr =  (0, 1, 1, 1,)

    nn = S2sNp(len(in_orarr), 1)
    for aa in range(len(in_orarr)):
        nn.memorize(in_orarr[aa], ou_orarr[aa])

    for cnt, aa in enumerate(tin_orarr):
        ttt = time.time()
        nn.recall(aa)
        print(nn.outputs, tou_orarr[cnt])
        assert nn.outputs == tou_orarr[cnt]
    #assert 0

def test_and():

    in_andarr =  (arr_0, arr_1,  arr_2,  arr_3,)
    ou_andarr =  (0, 0, 0, 1)
    tin_andarr =  ((0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_andarr =  (0, 0, 0, 1)

    nn = S2sNp(len(in_andarr), 1)
    for aa in range(len(in_andarr)):
        nn.memorize(in_andarr[aa], ou_andarr[aa])

    for cnt, aa in enumerate(tin_andarr):
        ttt = time.time()
        nn.recall(aa)
        print(nn.outputs, tou_andarr[cnt])
        assert nn.outputs == tou_andarr[cnt]
    #assert 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog='neunp',
                    description='S2S (sequence to sequence) neural numpy demo of OR and AND gate logic',
                    epilog='')
    parser.add_argument('-c', '--count',
                    help = "Number of gate inputs", default=2, type=int)
    parser.add_argument('-t', '--time', default=0, action="store_true",
                    help = "Show timing of the operations")

    args = parser.parse_args()

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
