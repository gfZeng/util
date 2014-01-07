#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#######################################################
# @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
# @Setup Time:   Tuesday,  7 January 2014.
# @Updated Time: 2014-01-08 00:25:30
# @Description:  
#######################################################

from util import *

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

def test():
    print "It's just a test"

if __name__ == '__main__':
    print slurp("unicode.txt")
    add_to_blacklist({'url': 'g', 'period': 5})
    time.sleep(10)
    add_to_blacklist({'url': 'g', 'period': 1})
    time.sleep(10)
    add_to_blacklist({'url': 'g', 'period': 1, 'cancel': 'true'})

