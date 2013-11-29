#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from util import *
import urllib2
import json
from bs4 import BeautifulSoup
from bs4.element import Tag

def fetch(url, encoding="utf-8", timeout=None):
    f = None
    try:
        f = urllib2.urlopen(url, timeout=timeout)
        return f.read().decode(encoding)
    finally:
        if f != None: f.close()

def is_dostream(l):
    return type(l) is tuple

def select(node, sel):
    return node.select(sel)

def text(node):
    return node.text

def texts(nodes):
    return map(text, nodes)

get = dict.__getitem__

def key(item):
    return item[0]

def val(item):
    return item[1]

def attrs(node):
    return node.attrs

def find_all(node, tag, attrs):
    node.find_all(tag, **attrs)

def extract(node, map_rules):
    if type(map_rules) is list:
        ret = []
        for rule in map_rules:
            ret.append(extract(node, rule))
        return ret
    ret = {}
    for k, v in map_rules.items():
        if is_dostream(k):
            ret.update(extract(dostream(node, *k), v))
        elif is_dostream(v):
            ret[k] = dostream(node, *v)
        elif type(v) is str:
            ret[k] = v
        else:
            ret[k] = extract(node, v)
    return ret

def nth(l, idx): return l[idx]

def first(l): return l[0]

def second(l): return l[1]

def last(l): return l[-1]

def pam(nodes, map_rules):
    return map(lambda node: extract(node, map_rules), nodes)

def select_one(node, sel, idx=0): return node.select(sel)[idx]

def str_strip(string): return string.strip()

def split(string, regex): return string.split(regex)

def test():
    '''
    map_rules = {'a': "good",
                 'b': [(select, "td.title a"), texts,]}
    x = extract(BeautifulSoup(fetch("https://news.ycombinator.com/")),
                map_rules)
    '''
    map_rules = {
        "providers": {
            'site': 'sohu.com',
            'title': '搜狐',
            'episodes': ((select, "div.pp.similarLists"),
                         first,
                         (select, "ul > li"),
                         (pam, {
                             'intro': '',
                             'source': ((select_one, 'a'),
                                 (Tag.get, 'href')),
                             'poster': ((select_one, 'img'),
                                 (Tag.get, 'src'))
                             })),
            },
        ((select, "div.blockRA"), first): {
            'title': ((select_one, 'h2 span'), text, str_strip),
            'language': '',
            'year': ((select, "div.cont > p"), (nth, 2), (select_one, "a"),
                     text,
                     (split, u"年"), first, int,),
            'rating': ((select_one, "div.mark"), text),
            'director': ((select_one, "div.cont p"), (select, "a"), texts),
            'actors': ((select_one, "div.cont p", 1), (select, "a"), texts)
            }
        }
    x = extract(BeautifulSoup(fetch(
                    "http://tv.sohu.com/s2013/jrshqpln/", "gbk")),
                map_rules)
    print json.dumps(x)

if __name__ == '__main__':
    test()
    #print "good"
