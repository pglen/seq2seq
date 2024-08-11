
import os, sys

sys.path.append("..")

import s2sutil

# Test suite

def test_pn():
    ret = s2sutil.pn(1/3)
    assert ret, "0.33"


def test_randmemb():
    www = s2sutil.randmemb( (1,2,3) )
    ret = www==1 or www==2 or www==3
    assert ret

def test_is_ok():
    ret = s2sutil.is_ok(1, 0)
    assert ret == '\x1b[31;1mERR\x1b[0m'
    ret = s2sutil.is_ok(1, 1)
    assert ret == '\x1b[32;1mOK\x1b[0m'

def test_lowpass():
    arr = (1, 2, 9, 22, 200)
    ret = s2sutil.lowpass(arr, 2)
    assert [1, 5, 31, 102, 200] == ret

def test_falledges():
    arr = (0, 0, 99, 22, 200)
    ret = s2sutil.falledges(arr)
    assert ret == [0, 0, True, 0, 0]

def test_raiseedges():
    arr = (0, 0, 99, 22, 11)
    ret = s2sutil.raisededges(arr)
    assert ret == [0, 0, True, 0, 0]

def test_rle():

    arr = (1,1,1,1,1,3,3,3,3,4,5,6)
    ret = s2sutil.rle(arr)
    assert ret == [(6, 1), (4, 3), 4, 5]

def test_scale():

    arr = ((1,1,1), (2,2,2), (3,3,3) )
    ret = s2sutil.scale(arr, 5, 5)
    print(ret)
    assert 0

# EOF
