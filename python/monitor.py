#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#######################################################
# @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
# @Setup Time:   Tuesday,  7 January 2014.
# @Updated Time: 2014-01-08 01:37:16
# @Description:  
#######################################################

from util import *
import urllib2
import socket

def fetch(url, encoding="utf-8"):
    f = None
    for i in range(3):
        try:
            f = urllib2.urlopen(url, timeout=3)
            return f.read().decode(encoding)
        except socket.timeout as e:
            pass
        finally:
            f and f.close()
    raise socket.timeout("time out")

black_list = {}
def add_to_blacklist(item):
    black_name = black_list.get(item['url'])
    if black_name:
        if item.get('cancel'):
            black_name['monitor'].cancel()
        black_name['target'] = item
        black_name['monitor'].change_interval(item['period'])
    else:
        black_name = {}
        black_name['target'] = item
        black_list[item['url']] = black_name
        black_name['monitor'] = set_interval(test, 3)

@timing
def test(m):
    for i in range(10):
        m(fetch, ["http://www.funshion.com", "http://www.letv.com", "http://v.qq.com", "http://www.youku.com", "http://v.sohu.com"])

if __name__ == '__main__':
    test(pmap)
    test(map)
    #print slurp("unicode.txt")
    #add_to_blacklist({'url': 'g', 'period': 5})
    #time.sleep(10)
    #add_to_blacklist({'url': 'g', 'period': 1})
    #time.sleep(10)
    #add_to_blacklist({'url': 'g', 'period': 1, 'cancel': 'true'})

