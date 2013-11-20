#!/usr/bin/env python2

from util import *
import time

def _time(fn):
    def wrapped_fn(*args, **kwargs):
        t = time.time()
        ret = fn(*args, **kwargs)
        print 'Elapsed time:', time.time() - t
        return ret
    return wrapped_fn

def foo(x):
    time.sleep(3)
    return x + 1

@_time
def pmap_test():
    return pmap(foo, [7, 8, 9])

@_time
def map_test():
    return map(foo, [7, 8, 9])

def test():
    print pmap_test()
    print map_test()

if __name__ == '__main__':
    test()
