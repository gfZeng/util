#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#######################################################
# @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
# @Setup Time:   Saturday, 30 November 2013.
# @Updated Time: 2013-11-30 16:55:26
# @Description:  
#######################################################

from util import *
import time
import urllib2

@timing
def test():
    pcall([foo for i in range(10)])

def foo():
    time.sleep(3)
    print "good"


def fetch(url):
    f = None
    try:
        f = urllib2.urlopen(url)
        return f.read()
    finally:
        f and f.close()

@timing
def test_map(mapfn):
    mapfn(fetch, ["http://v.qq.com/variety/type/list_-1_0_%d.html" % i for i in range(30)])

if __name__ == '__main__':
    #test_map(pmap)
    test_map(map)
