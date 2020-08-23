# coding: utf-8
from multiprocessing import Pool, cpu_count
import os
import time
import math
import logging


def task_func(data):
    print("pid {} data {}".format(os.getpid(), data))


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


class RunProcessTask():
    cpu_num = cpu_count()

    def __init__(self, task_data, run_task_func, proceee_cpu_time=1):
        """
        100个url，2个cpu，进程数是CPU数的3倍，每个进程分 100/(2*3)
        """
        # 开启的进程数
        process_num = self.cpu_num * proceee_cpu_time
        task_data = self.split_data(task_data, int(math.ceil(
            len(task_data) / process_num)))
        pool = Pool(process_num)
        result = []
        print(run_task_func)
        for data in task_data:
            result.append(pool.map_async(run_task_func, data))
        pool.close()
        pool.join()

    def split_data(self, data, per_size=10):
        target_list = []
        for i in range(int(math.ceil(len(data) / per_size))):
            start = i * per_size
            if start + per_size < len(data):
                end = start + per_size
            else:
                end = len(data)
            per_list = data[start:end]
            if per_list:
                target_list.append(per_list)
        return target_list


if __name__ == '__main__':
    data = [x for x in range(100)]
    task = RunProcessTask(data, task_func, 2)
