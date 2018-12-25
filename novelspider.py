# -*- coding:utf-8 -*-
'''
异步爬小说，程序爬取的目标网站新笔趣阁http://www.xbiquge.la/
'''

import time
import aiohttp
import asyncio
from lxml import etree
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse

# 头信息
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

# 获取网页（文本信息）
async def crawl(session, url):
    async with session.get(url[1]) as response:
        html = await response.text(encoding='utf-8')  #编码一定不要搞错
        await asyncio.sleep(0.1)  # 稍微设置点延迟
    await parser(html,url[0])

# 解析网页
async def parser(html,seq):

    try:
        #xphtml = etree.HTML(html)
        soup = BeautifulSoup(html, 'lxml')#本来用xpath的，但是老是报错不知道什么情况，bs就没问题，不知道什么情况
        # 获取网页中的章节名称和内容
        chaptername = soup.find('h1').text
        content = soup.find('div', id = 'content').text
        #chaptername = xphtml.xpath('//div[@id="wrapper"]/div[4]/div/div[2]/h1/text()')[0]
        #element_content = xphtml.xpath('//div[@id="content"]')[0]
        #content = element_content.xpath('string(.)')
        content = chaptername + '\n' + content + '\n\n'
        novel[seq] = content
    except:
        print(u'第' + str(seq+1) + u'章下载失败！')#小说序号跟章节对应不一定准确，有可能有偏移，有的小说开始会有几章非正文的东西，没有做过滤



async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [loop.create_task(crawl(session,url)) for url in urls] #新建任务列表
        await asyncio.wait(tasks) #开始任务，等待任务完成，这里返回两个列表，但本程序不需要用到，所以没接收变量

        

if __name__ == "__main__":
    # 统计该爬虫的消耗时间
    print('#' * 50)
    t1 = time.time() # 开始时间

    novel = {}#存储小说内容的
    urls = []#存储小说章节序号和链接，保证小说写入文本按照章节顺序

    src_url = 'http://www.xbiquge.la/0/951/'  #小说目录页面url
    target_req = request.Request(url = src_url,headers=headers)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('utf-8','ignore')  #编码一定不要搞错

    xhtml = etree.HTML(target_html)
    # 获取网页中的novel名称和章节链接
    novel_name = xhtml.xpath('//div[@id="info"]/h1/text()')[0]  
    novel['name'] = '*' * 10 + novel_name + '*' * 10 + '\n'
    #返回章节链接列表list[]
    novel_chapterlinks = xhtml.xpath('//div[@id="list"]/dl/dd/a[contains(@href,"/0/951")]/@href')
    
    for i in range(len(novel_chapterlinks)):
        urls.append((i,parse.urljoin(src_url,novel_chapterlinks[i])))
    
    

    loop = asyncio.get_event_loop()#定义loop
    loop.run_until_complete(main())#等待异步函数完成
    #loop.close()

    with open('all.txt','w',encoding='utf-8') as fw:    #编码一定不要搞错
        fw.write(novel['name'])
        for iw in range(len(novel)-1):
            try:
                fw.write(novel[iw])
            except:
                pass

    t2 = time.time() # 结束时间
    print('使用aiohttp，总共耗时：%s' % (t2 - t1))
    print('#' * 50)
