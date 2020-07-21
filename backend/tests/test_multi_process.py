from multiprocessing import Process
import os
import time
import requests


def long_time_task(url):
    print('子进程: {} - 任务{}'.format(os.getpid(), url))
    r = requests.get(url)
    print(r.text[100:120])
    print("结果: {}".format(8 ** 20))


if __name__ == '__main__':
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    urls = ['http://zhihu.com', 'http://baidu.com', 'http://taobao.com']
    for url in urls:
        p = Process(target=long_time_task, args=(url,))
        p.start()
        p.join()
    end = time.time()
    print("总共用时{}秒".format((end - start)))
