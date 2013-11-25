#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from util import *
import urllib2
import json
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag

def fetch(url, encoding="utf-8", timeout=None):
    f = None
    try:
        f = urllib2.urlopen(url, timeout=timeout)
        return f.read().decode(encoding)
    finally:
        if f != None: f.close()

def is_dostream(l):
    return type(l) is tuple

def unit_select(node, sel):
    if sel.startswith('#'):
        return node.findAll(id=sel[1:])
    sels = sel.split('.')
    tag = sels[0]
    class_ = " ".join(sels[1:])
    return node.findAll(tag, class_=class_)

def findAll(node, *args, **kwargs):
    return node.findAll(*args, **kwargs)

def tag_with_classes(tag, tagname, classes):
    try:
        if not classes:
            return tag.name == tagname
        return (
            tag.name == tagname
            and classes.issubset(
                set(dict(tag.attrs)['class'].split())))
    except:
        return False

def findChildren(node, *args, **kwargs):
    return node.findChildren(*args, **kwargs)

def map_unit_select(nodes, sel):
    if sel.startswith('#'):
        return map(findAll, nodes, id=sel[1:])

    sels = sel.split(".")
    tagname = sels[0]
    classes = set(sels[1:])
    find_func = findAll
    if tagname[0] == '>':
        tagname = tagname[1:]
        find_func = findChildren
    return reduce(
        list.__add__,
        map(
            lambda node: find_func(
                node,
                lambda tag: tag_with_classes(
                    tag, tagname, classes)),
            nodes),
        [])

def select(node, sel):
    if type(node) is list:
        nodes = node
    else:
        nodes = [node]
    sel = " ".join(sel.split())
    sel = sel.replace('> ', '>')
    sel_stream = sel.split()
    return reduce(lambda nodes, util_sel: map_unit_select(nodes, util_sel),
                  sel.split(),
                  nodes)

def text(node): return node.text

def texts(nodes): return map(text, nodes)


def attrs(node): return node.attrs

def find_all(node, tag, attrs): node.find_all(tag, **attrs)

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

def pam(nodes, map_rules):
    return map(lambda node: extract(node, map_rules), nodes)

def select_one(node, sel, idx=0): return select(node, sel)[idx]

def str_strip(string): return string.strip()

def split(string, regex): return string.split(regex)
def re_split(string, pattern):
    return re.split(pattern, string)

def test():
    '''
    map_rules = {'a': "good",
                 'b': [(select, "td.title a"), texts,]}
    x = extract(BeautifulSoup(fetch("https://news.ycombinator.com/")),
                map_rules)
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
                                        (Tag.get, 'src'))}),),
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
    '''
    map_rules = {
            ((select_one, "div.film_information"),
             (select_one, "div.pd19_noTop")): {
                 "index_page": "",
                 "update_date": "",
                 ((select_one, "div"), (select_one, "p span", 1),
                  text, (re_split, ur"年|月|日")): {
                     "publish_date": ("".join,),
                     "year": (first,)
                     },
                 "director": ((select_one, "div", 1), (select_one, "p"), (select, "a"), texts),
                 "type": ((select_one, "div", 1), (select_one, "p", 1), (select, "a"), texts),
                 "actors": ((select_one, "div", 2), (select, "a"), texts),
                }
            }
    x = extract(BeautifulSoup(fetch(
                    "http://www.iqiyi.com/v_19rrhfjhtc.html")),
                map_rules)
    print json.dumps(x)

if __name__ == '__main__':
    test()
