# python-
练习并完善python爬虫
----------------------------------
Crawler.py:
    对获取的url进行处理
        |-> 从respone中获取新的urls
        |-> 获取需要的内容(主要重写parse_page)

Scraper.py:
    对crawler线程的管理：
        |-> 分配urls给Crawler去处理
    对内存的及时清理：
        |-> Check() 检查result_urls_queue是否需要写入硬盘，检查程序是否已经完成任务。