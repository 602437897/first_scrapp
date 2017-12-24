import scrapy
from scrapy.selector import Selector
import os
import requests
from bs4 import BeautifulSoup
from threading import Thread
from test1.items import Test1Item

host = ''


def get_url():
    url = ''
    response = requests.get(url)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, features='html.parser')
    target = soup.find_all('tr', class_='tr3')
    li = []
    for i in target:
        he = 'http://' + host + '/' + i.find('a').attrs['href']
        if he.find('htm_data'):
            li += [he]
    return li


def write_file(path, filecontent):
    with open(path, 'ab') as f:
        f.write(bytes(filecontent+'\n', encoding='utf8'))


def write_image(path, filecontent):
    with open(path, 'wb') as f:
        f.write(filecontent)


def get_image(img, filename):
    url = img.xpath('@src').extract()[0]
    imgname = url.split('/')[-1]
    if not os.path.exists('img'):
        os.mkdir('img')
    if not os.path.exists('txt'):
        os.mkdir('txt')
    imgpath = 'img/' + imgname
    res = requests.get(url)
    if res.status_code == 200:
        th1 = Thread(target=write_image, args=(imgpath, res.content))
        th2 = Thread(target=write_file, args=(filename, url))
        th1.start()
        th2.start()


class DmozSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = [host]
    start_urls = get_url()

    def parse(self, response):
        images = Selector(response).xpath('//div[@class="tpc_content do_not_catch"]/img')
        fileurl = response.url
        filename = 'txt/' + response.url.split('/')[-1].split('.')[0] + '.txt'
        if not os.path.exists('txt'):
            os.mkdir('txt')
        with open(filename, 'wb') as f:
            f.write(bytes(fileurl + '\n', encoding='utf8'))
        for img in images:
            th = Thread(target=get_image, args=(img, filename))
            th.start()
