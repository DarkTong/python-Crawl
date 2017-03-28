from Crawler import Crawler

class MyWorker(Crawler):
    "根据具体情况去复写Crawler中的函数"
    def __init__(self, url=""):
        super(MyWorker, self).__init__(url)
    