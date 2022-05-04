#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aiohttp_sample_00.py
@Time    :   2022/05/03 18:49:56
@Author  :   Jerome
@Version :   1.0
@Contact :   jerome.lzh@gmail.com
@License :   GPL-3.0
@Desc    :   None
'''

# here put the import lib

import asyncio
import re
import time
import aiohttp
from lxml import html
from bs4 import BeautifulSoup
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

bookurl = 'https://www.xbiquge.so/book/49099/'

async def get_index():
    #! Get the index of the article
    async with aiohttp.request('get', url = bookurl) as response:
        page_text = await response.text()
        result = re.findall(r'<dd><a href="(.*?)">(.*?)</a></dd>', page_text)
        return result

async def get_article(page_url, title):
    #! Get the article
    cs = aiohttp.ClientSession()
    async with cs.request('get', url = page_url, header = headers) as response:
        # content = await response.text()
        content = await response.read()
        # result = re.findall(r'<div id="content" name="content">(.*?)</div>', content, re.S)
        # result = re.findall(r'<div id="content" name="content">(.*?)</div>', content)
        # result = ''.join(result)
        tree = html.fromstring(content)
        result = tree.xpath('//*[@id="content"]/text()')  #! xpath string for //*[@id="content"]
        # result = BeautifulSoup(result)
        text = ''.join(result[1:])
        with open(title + '.txt', 'wb') as f:
            f.write(text)

async def main():
    #! Main function
    index = await get_index()
    for page_url, title in index:
        page_url = bookurl + page_url
        article = await get_article(page_url, title)
        print(page_url, title)
    print(index)

    # for i in index:
        # print(i)

start_time = time.time()
asyncio.run(main())
print('Time: %s' % (time.time() - start_time))