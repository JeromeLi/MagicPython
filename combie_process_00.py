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
from tkinter import W

bn = '第一序列'
os.chdir(bn)

def title_name(name):
    tn = os.path.split(name[1:])[1][:-4]
    return tn

def combie(filename):
    with open(filename) as fr:
        file_contents = fr.read()
        tn = title_name(filename)
        text = tn + '\n\n' + file_contents + '\n\n\n'
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

print(f'Processing {bn} 1-9 chapters...')
article_combie(1)

print(f'Processing {bn} 10-99 chapters...')
article_combie(2)

print(f'Processing {bn} 100-999 chapters...')
article_combie(3)

print(f'Processing {bn} 1000-9999 chapters...')
article_combie(4)

# for name in sorted(glob.glob('./[0-9][0-9]、*.txt')):
#     print(f'{name}')

# for name in sorted(glob.glob('./[0-9][0-9][0-9]、*.txt')):
#     print(f'{name}')

# for name in sorted(glob.glob('./[0-9][0-9][0-9][0-9]、*.txt')):
#     print(f'{name}')


# for i in range(1,10000):
#     with open(f'{i}.txt', 'r') as f:
#         f.write(f'{i}')