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

bookurl = 'https://www.xbiquge.so/book/49099/'

async def get_index():
    #! Get the index of the article
    async with aiohttp.request('get', url = bookurl) as response:
        text = await response.text()
        result = re.findall(r'<dd><a href="(.*?)">(.*?)</a></dd>', text)
        return result

async def get_article(page_url, title):
    #! Get the article
    async with aiohttp.request('get', url = page_url) as response:
        response.encoding = 'GBK'
        text = await response.text()
        result = re.findall(r'<div id="content" name="content">(.*?)</div>', text, re.S)
        result = ''.join(result)
        with open(title + '.txt', 'w') as f:
            f.write(result)

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