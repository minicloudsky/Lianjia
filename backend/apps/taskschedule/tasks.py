import time

from celery import shared_task

from ershoufang_crawler import ErShouFangCrawler


@shared_task(name="test_task")
def my_task():
    with open('yeah.txt', 'w') as f:
        f.write(str(time.time()))
    return "success"


@shared_task(name="crawl_ershoufang")
def crawl_ershoufang():
    crawler = ErShouFangCrawler()
    return "finish crawl ershoufang ."
