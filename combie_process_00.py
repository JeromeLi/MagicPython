#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   combie_process_00.py
@Time    :   2022/05/07 12:17:20
@Author  :   Jerome
@Version :   1.0
@Contact :   jerome.lzh@gmail.com
@License :   GPL-3.0
@Desc    :   None
'''

# here put the import lib

import os
import re
import glob
import asyncio
from aiohttp_sample_01 import get_bookname as gbn

# os.chdir(bn)
bn = asyncio.get_event_loop().run_until_complete(gbn())

def title_name(name):
    tn = os.path.split(name[1:])[1][:-4]
    return tn

def combie(filename):
    with open(filename) as fr:
        file_contents = fr.read()
        tn = title_name(filename)
        tn_num = re.split(r'\W+',tn)[0]
        tn_article = re.split(r'、',tn)[1]
        full_chapter_name = '第' + tn_num + '章' + '  ' + tn_article
        print(f'{tn} =====>> {full_chapter_name}')
        text = full_chapter_name + '\n\n' + file_contents + '\n\n\n'

    with open(bn + '.txt', 'a') as fw:
        fw.write(text)

    return

def article_combie(n):
    if n == 1:
        for fn in sorted(glob.glob('./[0-9]、*.txt')):
            combie(fn)
    elif n == 2:
        for fn in sorted(glob.glob('./[0-9][0-9]、*.txt')):
            combie(fn)
    elif n == 3:
        for fn in sorted(glob.glob('./[0-9][0-9][0-9]、*.txt')):
            combie(fn)
    elif n == 4:
        for fn in sorted(glob.glob('./[0-9][0-9][0-9][0-9]、*.txt')):
            combie(fn)
    else:
        pass

    return

print('Current Dir:', os.getcwd())

filename = bn + '.txt'
if os.path.exists(filename) == False:
    print(f'Processing {bn} 1-9 chapters...')
    article_combie(1)

    print(f'Processing {bn} 10-99 chapters...')
    article_combie(2)

    print(f'Processing {bn} 100-999 chapters...')
    article_combie(3)

    print(f'Processing {bn} 1000-9999 chapters...')
    article_combie(4)
else:
    print(f'{filename} Already exists! Skip!')

