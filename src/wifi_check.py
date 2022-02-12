# -*- coding: utf-8 -*-

import socket
import time

TEST_SERVER = "www.google.com"

def is_connected():

  try:
    host = socket.gethostbyname(TEST_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def loop_until_connected():

    print('Internet connection check')
    while(not is_connected()):
        print('Connecting...')
        time.sleep(1)
    print('Connected to internet!')

if __name__ == '__main__':
    
    loop_until_connected()