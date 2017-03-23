#-*- coding:utf-8 -*-

import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class Crawler(object):
    "对网页的具体操作，工作者"
    def __init__(self, url=''):
        self.target_url = url
        (self.scheme, self.netloc) = urlparse(url)[0:2]

        self.respone = None
        self.soup = None

        self.url_in_site = set()
        self.url_out_site = set()

    #通过当前方法读取html
    def __get_html_data(self):
        if self.respone is None:
            try:
                self.respone = requests.get(self.target_url, timeout=5)
            except:
                return ""
        print("[_] Got respone")
        return self.respone.text

    #获取Soup
    def __get_soup(self):
        if self.soup is None:
            text = self.__get_html_data()
            if text != "":
                self.soup = BeautifulSoup(text)

    #获取所有url
    def __get_all_urls(self):
        self.__get_soup()
        if isinstance(self.soup, type(None)):
            return []
        else:
            url_lists = []
            all_tags = self.soup.findAll(name='a')
            scheme_mode = re.compile('^https?')
            for tag in all_tags:
                #scheme, netloc, path 三者的情况 -》 6种
                par = urlparse(tag['href'])
                tmp = ""
                if par.path != "" and par.path[0] != '/':
                    tmp = '/'
                #https/http开头的
                if par.scheme == "" and par.netloc == "" and par.path != "":
                    url_lists.append(self.scheme+'://'+self.netloc+tmp+par.path)
                elif par.scheme != "" and par.netloc != "" and par.path != "":
                    if re.match(scheme_mode, par.scheme) is not None:
                        url_lists.append(par.scheme+'://'+par.netloc+tmp+par.path)
                #待补充
            return url_lists

    #分类url
    def __get_urls_inpage(self):
        url_lists = self.__get_all_urls()

        for url in url_lists:
            par = urlparse(url)
            if self.netloc in par[1]:
                self.url_in_site.add(url)
            else:
                self.url_out_site.add(url)

    def parse_page(self):
        "#过滤出自己想要的url,重写"
        return self.url_in_site

    def execute(self):
        "#执行"
        self.__get_urls_inpage()
        result_url = self.parse_page()
        return result_url

def debug():
    "调试"
    begin_url = 'http://gzhu.edu.cn'
    crawler = Crawler(begin_url)
    urls = crawler.execute()
    with open('urlsite', 'w') as site:
        for url in urls:
            site.write(url+'\n')

if __name__ == '__main__':
    debug()
