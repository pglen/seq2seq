#!/usr/bin/env python

import sys, random
from collections import defaultdict

#def isiter(self, varx):
#    try:
#        iter(varx)
#        return True
#    except TypeError:
#        #print('not iterable')
#        pass

class DeepDict(defaultdict):

    ''' Dictionary to automatically create new dimensions
    '''

    def __init__(self, keyx = None, valx = None):

        super().__init__()
        #keyx, valx)

        print("__init__ keyx:", keyx, "valx:", valx)
        if keyx and valx:
            self.setdeep(keyx, valx)
        elif keyx and isinstance(keyx, dict):
            for ccc in keyx:
                self.__setitem__(ccc, keyx[ccc])
        elif keyx and (isinstance(keyx, list) or isinstance(keyx, tuple)):
            cnt = 0; kkk = 0
            for cccc in keyx:
                if cnt % 2 == 0:
                    kkk = cccc
                if cnt % 2 == 1:
                    self.__setitem__(kkk, cccc)
                cnt += 1
        else:
            # Empty constructor
            pass

    def setdeep(self, dims, val):
        print("setdeep", dims)
        hist = self
        for cnt, aa in enumerate(dims):
            if cnt == len(dims)-1:
                if aa in hist:
                    if isinstance(hist[aa], dict):
                        #print("Warn: key exists", aa)
                        raise ValueError("Dimension exists already", aa)

                hist.setdefault(aa, val)
            else:
                if not aa in hist:
                    # Create if not present
                    hist.setdefault(aa, {})
            hist = hist[aa]

    def getdim(self, dim):

        ''' Get value for dimention '''

        hist = self
        for aa in dim:
            # Generate exception if not in dict
            if isinstance(hist[aa], dict):
                pass
            hist = hist[aa]

        #for bb in hist:
        #    print(bb)
        return hist

    def recurse(self, idx = [], callb = None):
        #print("recurse ttt:", self)
        #print("recurse idx =", idx)
        nnn = self
        # Build index
        for aaa in idx:
            #if aaa in nnn:
            if isinstance(nnn[aaa], dict):
                nnn = nnn[aaa]
        #print("nnn =", nnn)
        for aaaa in nnn:
            #print("re", aaaa)
            if isinstance(nnn[aaaa], dict):
                idx.append(aaaa)
                idx = self.recurse(idx, callb)
            else:
                idx2 = idx + [aaaa,]
                #print("idx =", idx2, "val =", nnn[aaaa])
                if callb:
                    callb(idx2, nnn[aaaa])
        # back out
        return idx[:len(idx)-1]

    def update(self, *args, **kwargs):
        print("update", keyx, valx)

    def __getitem__(self, key):
        print("getitem key =", key)
        ret = super().__getitem__(key)

    def __setitem__(self, key, value):
        print("setitem", key, type(key), value, type(value))
        ret = super().__setitem__(key, value)

    #def __delitem__(self, key, value):
    #    if isinstance(key, tuple):
    #        for k in key: super().__delitem__(k)
    #    else:
    #        super().__setitem__(key, value)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    import  pgutil

    zzz = defaultdict(dict)
    zzz[1][2] = 5
    print(zzz)
    zzz[1][2] = 'b'
    zzz[1][3][4] = 'd'
    print(zzz)
    print(33)

    mmm = DeepDict( { 0 : "aaa"} )
    print("mmm =", mmm)
    aaa = DeepDict( ( 9  , "ddd") )
    print("aaa =", aaa)
    aaa = DeepDict( [ 99  , "dddd",] )
    print("aaa =", aaa)

    nnn = DeepDict( {(1,2,3,4) : "aaa", (1,2,3,5) : "bbb"} )
    print("nnn =", nnn)

    def callit(idx, val):
        print("  callb:", idx, val)
    ttt = DeepDict()
    ttt.setdeep((1, 1, 3, 4), 'a')
    ttt.setdeep((1, 2, 3, 5), 'b')
    ttt.setdeep((1, 2, 6), 'c')
    ttt.setdeep((1, 3,), 'c')
    print("ttt =", ttt)
    ttt.recurse(callb=callit)

    print("getdim[1.2]:", ttt.getdim((1,2 )))
    print("getdim[1,2,3]:", ttt.getdim((1,2,3 )))
    print("getdim[1,1,3,4]:", ttt.getdim((1,1,3,4 )))

# EOF
