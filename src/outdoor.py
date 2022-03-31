# -*- coding: utf-8 -*-

import json
import requests
import time

import config as cfg


url = 'http://studenci.fuw.edu.pl/~pablo/luftdaten/temp.json'
tab_name = 'main'
device = 'DHT11'
localization = 'FUW_roof'
time_delay = 60*10

def log_outdoor():

    r = requests.get(
        url,
        params={}
    )

    data = json.loads(r.text)
    temperature = data['sensordatavalues'][2]['value']
    humidity = data['sensordatavalues'][3]['value']

    requests.get(
        'http://{0}:{1}/data'.format(*cfg.SERVER_ADDRESS),
        params = {
            'tab_name' : tab_name,
            'device' : device,
            'localization' : localization,
            'temperature' : temperature,
            'humidity' : humidity
        }
    )
    print('Outdoor temperature and humidity logged')

def logger_outdoor():

    while True:
        log_outdoor()
        time.sleep(time_delay)

def main_outdoor():

    time.sleep(cfg.THREAD_DELAY)

    logger_outdoor()

    