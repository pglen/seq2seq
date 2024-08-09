#!/usr/bin/env python

import sys, random

#def isiter(self, varx):
#    try:
#        iter(varx)
#        return True
#    except TypeError:
#        #print('not iterable')
#        pass

class DeepDict(dict):

    ''' Dictionary to automatically create new dimensions from tuple
        based keys.
    '''

    def __init__(self, keyx = None, valx = None):
        #print("keyx", keyx, "valx", valx)
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
        #print("setdeep", dims)
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

    def __getitem__(self, key):
        #print("getitem key =", key)
        if isinstance(key, tuple):
            ret = self.getdim(key)
        else:
            if key not in self:
                super().setdefault(key, {})
            ret = super().__getitem__(key)
        return ret

    def __setitem__(self, key, value):
        #print("setitem", key, type(key), value, type(value))
        if isinstance(key, tuple):
            #print("tuple", key)
            self.setdeep(key, value)
        else:
            try:
                super().__getitem__(key)
            except:
                #pgutil.print_exception("set -> get")
                #print("set", sys.exc_info())
                if value:
                    super().__setitem__(key, value)
                else:
                    super().__setitem__(key, {})

    #def __delitem__(self, key, value):
    #    if isinstance(key, tuple):
    #        for k in key: super().__delitem__(k)
    #    else:
    #        super().__setitem__(key, value)

# Test suite

def test_construct():
    ddd = DeepDict((1,2,3,4), 111)
    assert ddd[1,2,3,4] == 111

def test_create():
    ddd = DeepDict()
    ddd[1,2,3] = 88;  ddd[1,2,4] = 99
    assert ddd[1] == {2: {3: 88, 4: 99}}
    assert ddd[1,2] == {3: 88, 4: 99}
    assert ddd[1,2,3] == 88
    assert ddd[1,2,4] == 99

def test_dump():
    ddd = DeepDict((1,2,3,4), 222)
    res = ""
    def callbx(key, val):
        nonlocal res
        res += str(key) + " " + str(val)
    ddd.recurse(callb=callbx)
    assert res == "[1, 2, 3, 4] 222"

def test_exc2():
    nn = DeepDict(); nn.setdeep((0,1,2), 123)
    exc = False
    try:    aa = nn[0,1,3]
    except: exc = True
    assert  exc == True

def test_exc2():
    nn = DeepDict(); nn.setdeep((0,1,2), 123)
    exc2 = False
    try:    nn.setdeep((0,), 'c')
    except: exc2 = True
    assert  exc2 == True

def test_one_level():
    nn = DeepDict(); nn.setdeep((0,), 'b')
    assert nn == {0:'b'}
    nnn = DeepDict()
    nnn[1,2,3,4] = 555
    assert nnn[1,2,3,4] == 555

# ------------------------------------------------------------------------

if __name__ == '__main__':

    import  pgutil

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
