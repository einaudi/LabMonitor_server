# -*- coding: utf-8 -*-

from http.server import HTTPServer
from server import ReqHandler

from src.memory_usage import main_mu
from src.wifi_check import loop_until_connected
import threading

import src.config as cfg


try:
    loop_until_connected()
    # Memory usage thread
    mu_thread = threading.Thread(target=main_mu)
    mu_thread.start()
    # Server
    print('Starting server on %s:%i...' % cfg.SERVER_ADDRESS)
    server = HTTPServer(cfg.SERVER_ADDRESS, ReqHandler)
    print('Running server (type Ctrl+C to exit)...')
    print('\n### Logs ###\n')
    server.serve_forever()
    print('End')
except KeyboardInterrupt:
    server.shutdown()
    mu_thread.join()
    print('End')
