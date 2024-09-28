#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import traceback, re

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class

class Config:

    def __init__(self, optarr):
        self.optarr = optarr

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            if aa[0] in optletters:
                print("Warning: duplicate option", "'" + aa[0] + "'")
            optletters += aa[0]
        #print optletters

        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError as err:
            print("Invalid option(s) on command line:", err)
            return ()

        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None:
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None:
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None:
                            self.optarr[bb][3]()
        return args

# ------------------------------------------------------------------------
# Print an exception as the system would print it

def print_exception(xstr = "exc", fp = sys.stdout):
    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print("Could not print trace stack. ", sys.exc_info())
    print(cumm, file=fp)

# ------------------------------------------------------------------------
# Never mind

def cmp(aa, bb):
    aaa = os.path.basename(aa);  bbb = os.path.basename(bb)
    pat = re.compile("[0-9]+")
    ss1 = pat.search(aaa)
    ss2 = pat.search(bbb)

    if(ss1 and ss2):
        aaaa = float(aaa[ss1.start(): ss1.end()])
        bbbb = float(bbb[ss2.start(): ss2.end()])
        #print aaa, bbb, aaaa, bbbb
        if aaaa == bbbb:
            return 0
        elif aaaa < bbbb:
            return -1
        elif aaaa > bbbb:
            return 1
        else:
            #print "crap"
            pass
    else:
        if aaa == bbb:
            return 0
        elif aaa < bbb:
            return -1
        elif aaa > bbb:
            return 1
        else:
            #print "crap"
            pass

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def  usleep(msec):

    if sys.version_info[0] < 3 or \
        (sys.version_info[0] == 3 and sys.version_info[1] < 3):
        timefunc = time.clock
    else:
        timefunc = time.process_time

    got_clock = timefunc() + float(msec) / 1000
    #print got_clock
    while True:
        if timefunc() > got_clock:
            break
        Gtk.main_iteration_do(False)

# -----------------------------------------------------------------------
# Call func with all processes, func called with stat as its argument
# Function may return True to stop iteration

def withps(func, opt = None):

    ret = False
    dl = os.listdir("/proc")
    for aa in dl:
        fname = "/proc/" + aa + "/stat"
        if os.path.isfile(fname):
            ff = open(fname, "r").read().split()
            ret = func(ff, opt)
        if ret:
            break
    return ret

def leadspace(strx):

    '''  Count lead spaces '''
    cnt = 0;
    for aa in range(len(strx)):
        bb = strx[aa]
        if bb == " ":
            cnt += 1
        elif bb == "\t":
            cnt += 1
        elif bb == "\r":
            cnt += 1
        elif bb == "\n":
            cnt += 1
        else:
            break
    return cnt

def is_ok(val, ref, okx = "OK", errx = "ERR"):
    ''' return "OK" if equal, ERR if different '''
    if val == ref:
        ret = "\033[32;1m%s\033[0m" % okx
    else:
        ret = "\033[31;1m%s\033[0m" % errx
    return ret

if __name__ == '__main__':

    print("Test pgutils:")
    try:
        raise(ValueError)
    except:
        print_exception("Test exception dump")

    from s2sutil import *
    lead = leadspace("   test leadspace")
    print("lead", lead, is_ok(lead, 3))

    ttt = time.time()
    usleep(20)
    ddd = 1000 * (time.time() - ttt)
    print("time diff: ", ddd, "ms", is_ok(True, (ddd >= 20)) )


# EOF
