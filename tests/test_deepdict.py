
import os, sys

sys.path.append("..")

from pgdict import *

# Test suite

def test_construct():
    ddd = DeepDict((1,2,3,4), 111)
    assert ddd[1,2,3,4] == 111
    assert ddd[1][2][3][4] == 111

#def test_construct2():
#    ddd = DeepDict()
#    ddd[1][2][3][4] = 111
#    assert ddd[1,2,3,4] == 111

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

def test_exc():
    nn = DeepDict(); nn.setdeep((0,1,2), 123)
    exc = False
    try:
        aa = nn[0,1,3]
    except:
        exc = True
        print(sys.exc_info())
    assert  exc == True

def test_exc2():
    nn = DeepDict(); nn.setdeep((0,1,2), 123)
    exc2 = False
    try:
        nn.setdeep((0,1), 'c')
    except:
        exc2 = True
        print(sys.exc_info())
    assert  exc2 == True

def test_exc3():

    ''' Access non existant members '''

    nn = DeepDict(); nn.setdeep((0,1,2), 123)
    exc2 = False
    try:
        nn.setdeep((0,), 'c')
    except:
        exc2 = True
        print(sys.exc_info())

    assert  exc2 == True

def test_one_level():
    nn = DeepDict(); nn.setdeep((0,), 'x')
    assert nn == {0:'x'}
    nnn = DeepDict()
    nnn[1,2,3,4] = 555
    assert nnn[1,2,3,4] == 555


