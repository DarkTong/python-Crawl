# -*- coding: utf-8 -*-

from queue import Queue
import threading
from Crawler import Crawler
import time

class Scraper(object):
    """
    管理线程池、分配任务、处理结果
    """
    def __init__(self, single_page=True, workers_num=8, worker_class=Crawler):
        self.count = 0 #计算url数目
        self.workers_num = workers_num #线程数

        """获得处理类"""
        self.worker_class = worker_class

        """check if the workers is die"""
        self.all_dead = False

        """ 检查结果队列正在输出 """
        self.is_outputing = False

        """store the visited pages"""
        self.visited = set()
        self.contain = set()

        """by Crawler's extension result queue"""
        self.result_urls_queue = Queue()
        self.result_elements_queue = Queue()

        """
        if single_page == Ture,
        the task_queue should store the tasks(unhandled)
        """
        self.task_queue = Queue()

        self.__init_workers()

    """
    init worker(s)
    """
    def __init_workers(self):
        for _ in range(self.workers_num):
            ret = threading.Thread(target=self._worker)
            ret.start()
        threading.Thread(target=self.Check()).start()

    def get_result_urls_queue(self):
        """返回结果队列"""
        return self.result_urls_queue
    
    def get_result_elements_queue(self):
        """返回元素队列"""
        return self.result_elements_queue
    
    def _worker(self):
        if self.all_dead is not False:
            self.all_dead = False
        
        crawler = None
        while not self.all_dead:
            try:
                #block=True,队列可中断，用于多线程
                url = self.task_queue.get(block=True)
                #if url in self.contain:
                #    self.contain.pop()
                print('Working', url)
                print('Task len', self.task_queue.qsize())
                print('result len', self.result_urls_queue.qsize())
                #check url has used?
                if url in self.visited:
                    continue
                
                self.count += 1
                print('Having process', self.count, 'Pages')
                self.visited.add(url)
                crawler = self.worker_class(url)
                result_url = crawler.execute()

                for url in result_url:
                    if url not in self.visited and url not in self.contain:
                        while self.is_outputing is True: pass
                        self.task_queue.put(url)
                        self.result_urls_queue.put(url)
                        self.contain.add(url)
                #释放变量、释放内存
                del result_url
                del crawler
            except:
                pass
            finally:
                pass

    """ 检查结果队列 """
    def Check(self):
        while self.all_dead:
            if self.result_urls_queue.qsize() > 5000:
                self.is_outputing = True
                with open('scraper.site', 'a') as File:
                    while self.result_urls_queue.empty() is False:
                        item = self.result_urls_queue.get()
                        File.write(str(item) + '\n')
                self.is_outputing = False
                # 判断是否已经搜索完毕
                cnt = 0
                while self.task_queue.empty() and cnt <= 5:
                    cnt += 1
                    time.sleep(5)
                if cnt == 5:
                    self.kill_workers()
    """
    scraper interface
    """
    def kill_workers(self):
        """杀掉线程"""
        if self.all_dead is False:
            self.all_dead = True
    
    def feed(self, target_urls):
        """一开始的url初始化"""
        for target in target_urls:
            self.task_queue.put(target)

    