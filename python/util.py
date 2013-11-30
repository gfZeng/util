#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#######################################################
# @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
# @Setup Time:   Saturday, 30 November 2013.
# @Updated Time: 2013-11-30 16:23:23
# @Description:  
#######################################################


import threading, Queue

class future(threading.Thread):

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
#deref = future.deref


def pmap(f, *seqs):
    return map(deref, map(lambda args: future(f, *args), zip(*seqs)))


############ p_map is not thread safe ##########
def p_map(f, seqs, pool_size=30):
    q = Queue.Queue(pool_size)
    ret = []
    argvs = zip(seqs)
    #argvs = seqs
    def worker():
        for argv in argvs:
            q.put(future(f, *argv))
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    class ResultSet(object):
        def __init__(self, q, capacity):
            self.q = q
            self.capacity = capacity
        def next(self):
            if self.capacity > 0:
                self.capacity -= 1
                return deref(self.q.get())
            raise Exception("no more elements", "idiot!!!")
        def has_next(self):
            return self.capacity > 0
    return ResultSet(q, len(argvs))
        

############################## Girl ################################
# Girl is a Observable object, implements by use Closure
####################################################################
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


'''
class Girl(object):
    def __init__(self, v):
        self.v = v
        self.wathers = []

    def add_watch(self, k, w):
        self.watchers.append(lambda r, ov, nv: w(k, r, ov, nv))

    def _notify_watchers(ov, nv):
        for w in self.watchers:
            try:
                w(self, ov, nv)
            except e:
                print e

    def reset(self, nv):
        ov = self.v
        self.v = nv
        _notify_watchers(ov, self.v)
        return nv

    def swap(self, fn, *args, **kwargs):
        ov = self.v
        self.v = fn(self.v, *args, **kwargs)
        _notify_watchers(ov, self.v)
        return nv
'''


def add_watch(g, k, w):
    g.add_watch(k, w)


def reset(g, no):
    g.reset(no)


def swap(g, fn, *args, **kwargs):
    g.swap(fn, *args, **kwargs)


def  inc(x):
    return x + 1


def dostream(ret, *ls):
    for l in ls:
        if hasattr(l, '__call__'):
            ret = l(ret)
        elif type(l) in (tuple, list):
            ret = l[0](ret, *l[1:]) 
        else:
            raise Exception("bad arguments", l)
    return ret

def donestream(ret, *ls):
    for l in ls:
        if hasattr(l, '__call__'):
            ret = l(ret)
        elif type(l) in (tuple, list):
            ret = l[0](*(l[1:]+type(l)((ret,)))) 
        else:
            raise Exception("bad arguments", l)
    return ret


def key(item): return item[0]
get = dict.__getitem__
def val(item): return item[1]
def nth(l, idx): return l[idx]
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]


def timing(f):
    def wrapped(*args, **kwargs):
        t = time.time()
        try:
            return f(*args, **kwargs)
        finally:
            print "Elapsed time:", time.time() - t, "msecs"
    return wrapped
