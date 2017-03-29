from Scraper import *
import time

if __name__ == '__main__':
    url = "http://gzhu.edu.cn"
    with open('scraper.site', 'w') as File: pass
    scraper = Scraper(False, 16)
    scraper.feed([url])
    time.sleep(1000)
    print("...")
    scraper.kill_workers()
    print("END")
    with open('scraper.site', 'w') as File:
        while scraper.result_urls_queue.qsize() is not 0:
            File.write(str(scraper.result_urls_queue.get())+'\n')
