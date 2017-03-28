from Scraper import *

if __name__ == '__main__':
    url = "http://gzhu.edu.cn"
    scraper = Scraper(False)
    scraper.feed(url)
    with open('scraper.site', 'w') as File:
        for item in scraper.result_urls_queue:
            f.write(item + '\n')
