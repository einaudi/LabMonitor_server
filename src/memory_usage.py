# -*- coding: utf-8 -*-

import os
import time
import json

import src.config as cfg

import requests


def init_mu():

    requests.get(
        'http://{0}:{1}/add_table'.format(*cfg.SERVER_ADDRESS),
        params={
            'tab_name' : cfg.MU_TABNAME,
            'col_settings' : json.dumps({
                'memory_free' : 'real',
                'memory_total' : 'real',
                'memory_usage' : 'real'
            }),
            'sensor' : 0
        }
    )

def get_mu():

    disk = os.statvfs('/')
    # Get data
    total = disk.f_blocks * disk.f_frsize
    free = disk.f_bavail * disk.f_frsize
    usage = 100 * (1-free/total)
    # Convert to GB
    free /= (2**30)

    return free, total, usage

def log_mu():
    free, total, usage = get_mu()

    requests.get(
        'http://{0}:{1}/data'.format(*cfg.SERVER_ADDRESS),
        params = {
            'tab_name' : cfg.MU_TABNAME,
            'memory_free' : free,
            'memory_total' : total,
            'memory_usage' : usage
        }
    )
    print('Memory usage logged')

def logger_mu():

    while True:
        log_mu()

        time.sleep(cfg.MU_SAVEEVERY)

def main_mu():

    time.sleep(cfg.THREAD_DELAY)

    init_mu()
    logger_mu()


if __name__ == '__main__':
    disk = os.statvfs('/')
    total = disk.f_blocks * disk.f_frsize
    free = disk.f_bavail * disk.f_frsize
    print("Total: {:.2f} GiB".format(total / (2**30)))
    print("Free: {:.2f} GiB".format(free / (2**30)))
    print("Usage: {:.2f} %".format(100*(1-free/total)))
