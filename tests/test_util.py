# Test suite

import os, sys

sys.path.append("..")

from pgutil import *

def test_lead():

    fff = leadspace("   deleted fromn")
    assert fff == 3

def test_exc():

    ref = \
    "hello <class 'ValueError'> \n"
    "File: pgutil.py Line.*\n"
    #"  Context: test_exc -> raise(ValueError)\n" \
    #".*"
    try:
        raise(ValueError)
    except:
        import tempfile
        fp, fname = tempfile.mkstemp() #"tmp.%d.txt" % os.getpid()
        #fpx = open(fname, "wt")
        fpx = os.fdopen(fp, "w")
        print_exception("hello", fp=fpx)
        fpx.close()
        #print(fname)
        fp2 = open(fname, "rt")
        sss = fp2.read()
        fp2.close()
        os.unlink(fname)

    print ("ref= [" + ref + "]")
    print ("sss= [" + sss + "]")
    mmm = re.match(ref, sss, flags = re.MULTILINE | re.DOTALL)
    #print(mmm)
    assert mmm

# EOF
