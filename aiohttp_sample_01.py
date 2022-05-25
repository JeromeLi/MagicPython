'''
Author: Jerome
Date: 2022-05-07 11:51:34
LastEditors: Jerome
LastEditTime: 2022-05-07 12:04:44
FilePath: /MagicPython/aiohttp_sample_01.py
Description:

Copyleft 2022 GPL-3.0.
'''
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
import os
import time
import aiohttp
import uvloop
from lxml import html

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

bookurl = 'https://www.xbiquge.so/book/49099/'

async def get_bookname():
    #! get the book name from the book url
    session = aiohttp.ClientSession()
    async with session.get(url = bookurl, headers = headers) as response:
        content = await response.read()
        tree = html.fromstring(content)
        result = tree.xpath('/html/body/div[2]/div[2]/div[2]/h1/text()')
        # await session.close()
        bookname = result[0]
        print(f'Book Name: {bookname}')
    await session.close()
    return bookname

async def book_dir(dirname):
    if os.path.exists(dirname) != True:
        print('Create Book Name Dir:', dirname)
        os.mkdir(dirname)
    os.chdir(dirname)
    print('Current Dir:', os.getcwd())
    filepath = os.getcwd()
    return filepath

async def get_index():
    #! Get the index of the article
    session = aiohttp.ClientSession()
    async with session.get(url = bookurl, headers=headers, verify_ssl=False) as response:
        page_text = await response.text()
        result = re.findall(r'<dd><a href="(.*?)">(.*?)</a></dd>', page_text)
        # await session.close()
        bn = await get_bookname()
        with open(bn + '_index.txt', 'w') as f:
            for page_url, title in result:
                page_url = bookurl + page_url
                f.write(page_url + '    ' + title + "\n")
        f.close()
    await session.close()
    return result

async def get_article(page_url, title, nb):
    #! Get the article
    page_url = bookurl + page_url
    target_dir = os.path.join(os.path.dirname(__file__) + '/' + nb + '/')
    filename = os.path.join(target_dir, title + '.txt')
    # os.chdir(target_dir)
    # print(f'Target dir: {target_dir}')

    try:
        # if os.getcwd() != os.path.dirname(filename):
        os.chdir(target_dir)
        if os.path.exists(filename) == False:
            # print(f'not found: {filename}')
            session = aiohttp.ClientSession()
            async with session.get(url = page_url, headers = headers, verify_ssl=False) as response:
                content = await response.read()
                tree = html.fromstring(content)
                result = tree.xpath('//*[@id="content"]/text()')  #! xpath string for //*[@id="content"]
                text = ''.join(result[1:])
                text = text.replace('\u00a0\u00a0\u00a0\u00a0', '\n')
                print(f'{time.strftime("%X")} --> {page_url} {title}')
                with open(title + '.txt', 'w') as f:
                    f.write(text)
                f.close()
                # title_text = title + '\n'
                # text = title_text + text
                # with open(nb + '.txt', 'a') as f:
                #     f.write(text)
            await session.close()
        else:
            print(f'{filename} Already exists! Skip!')
    except Exception:
        print(f'{page_url} {title} Error!')


# def callback_writefile (future):
#     print(f'{time.strftime("%X")} --> {future.result()}')
#     if os.getcwd() != os.path.dirname(filename):
#         os.chdir(os.path.dirname(filename))
#     else:
#         pass

#     with open(title + '.txt', 'w') as f:
#         f.write(text)
#     f.close()

# async def main_parallel():
#     index = await get_index()
    # task = []
    # # async with aiohttp.ClientSession() as session:
    # for page_url, title in index:
    #     task.append(get_article(page_url, title))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(*task, return_exceptions=True))
    # loop.close()

async def main():
    #! Main function
    nb = await get_bookname()
    await book_dir(nb)
    index = await get_index()
    task = []
    # async with aiohttp.ClientSession() as session:
    for page_url, title in index:
        task.append(get_article(page_url, title, nb))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(*task, return_exceptions=True))
    # loop.close()
    await asyncio.gather(*task, return_exceptions=True)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print('Time: %s' % (time.time() - start_time))