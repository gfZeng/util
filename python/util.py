#!/usr/bin/env python2

import threading

class fut(threading.Thread):
    def __init__(self, fn, *args, **kwargs):
        threading.Thread.__init__(self)
        self.fn = lambda: fn(*args, **kwargs)
        self.val = None
        self.start()
    def run(self):
        self.val = self.fn()
    def deref(self, timeout_ms=None, timeout_val=None):
        self.join(timeout_ms and (timeout_ms / 1000.0))
        if self.is_alive():
            return timeout_val
        return self.val
    def __call__(self):
        return self.deref()

def deref(f, timeout_ms=None, timeout_val=None):
    return f.deref(timeout_ms, timeout_val)

def pmap(f, *seqs):
    return map(deref, map(lambda args: fut(f, *args), zip(*seqs)))

class Girl(object):
    def __init__(self, o):
        self.o = o
    def reset(self, no):
        self.o = no
    def swap(self, fn, *args, **kwargs):
        self.o = fn(self.o, *args, **kwargs)
    def add_watch(self, k, watch):
        def wrap(fn):
            def nfn(*args, **kwargs):
                oo = self.o
                fn(*args, **kwargs)
                watch(k, self, oo, self.o)
            return nfn
        self.reset = wrap(self.reset)
        self.swap = wrap(self.swap)
    def deref(self):
        return self.o
    def __call__(self):
        return self.o

def add_watch(g, k, w):
    g.add_watch(k, w)

def reset(g, no):
    g.reset(no)

def swap(g, fn, *args, **kwargs):
    g.swap(fn, *args, **kwargs)

def  inc(x):
    return x + 1
