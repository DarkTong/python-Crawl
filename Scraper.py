# -*- coding: utf-8 -*-

from queue import Queue
import threading
from Crawler import Crawler

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

        """store the visited pages"""
        self.visited = set()

        """by Crawler's extension result queue"""
        self.result_urls_queue = Queue()
        self.result_elements_queue = Queue()

        """
        if single_page == Ture,
        the task_queue should store the tasks(unhandled)
        """
        self.task_queue = Queue()

        self.single_page = single_page
        if self.single_page is False:
            self.__init_workers()
        else:
            self.__init_single_worker()

    def __check_single_page(self):
        if self.single_page is True:
            raise Exception('[!]Single page won\'t allow you use many workers')

    """
    init worker(s)
    """
    def __init_single_worker(self):
        ret = threading.Thread(target=self._single_worker)
        ret.start()

    def __init_workers(self):
        self.__check_single_page()

        for _ in range(self.workers_num):
            ret = threading.Thread(target=self._worker)
            ret.start()

    def get_result_urls_queue(self):
        """返回结果队列"""
        return self.result_urls_queue
    
    def get_result_elements_queue(self):
        """返回元素队列"""
        return self.result_elements_queue
    
    def _single_worker(self):
        """worker function"""
        if self.all_dead is not False:
            self.all_dead = False
        
        crawler = None
        while not self.all_dead:
            try:
                url = self.task_queue.get(block=True)
                print('Working', url)
                try:
                    if url[:url.index('#')] in self.visited:
                        continue
                except:
                    pass

                if url in self.visited:
                    continue
                else:
                    pass
                
                self.count += 1
                print('Having process', self.count, 'Pages')
                crawler = self.worker_class(url)
                self.visited.add(url)
                result_url = crawler.execute()

                for url in result_url:
                    if url not in self.visited:
                        self.task_queue.put(url)
                        self.result_urls_queue.put(url)
            except:
                pass
            finally:
                pass
    
    def _worker(self):
        if self.all_dead is not False:
            self.all_dead = False
        
        crawler = None
        while not self.all_dead:
            try:
                #block=True,队列可中断，用于多线程
                url = self.task_queue.get(block=True)
                print('Working', url)
                try:
                    if url[:url.index('#')] in self.visited:
                        continue
                except:
                    pass

                if url in self.visited:
                    continue
                else:
                    pass
                
                self.count += 1
                print('Having process', self.count, 'Pages')
                crawler = self.worker_class(url)
                self.visited.add(url)
                result_url = crawler.execute()

                for url in result_url:
                    if url not in self.visited:
                        self.task_queue.put(url)
                        self.result_urls_queue.put(url)
            except:
                pass
            finally:
                pass

    """
    scraper interface
    """
    def kill_workers(self):
        """杀掉线程"""
        if self.all_dead is False:
            self.all_dead = True
    
    def feed(self, target_urls):
        """一开始的url初始化"""
        if isinstance(target_urls, list):
            for target in target_urls:
                self.task_queue.put(target)
        elif isinstance(target_urls, str):
            self.task_queue.put(target_urls)
        else:
            pass

    