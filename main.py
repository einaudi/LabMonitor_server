# -*- coding: utf-8 -*-

from http.server import HTTPServer
from server import ReqHandler

from src.wifi_check import loop_until_connected

import src.config as cfg


try:
    loop_until_connected()

    # Server init
    print('Starting server on %s:%i...' % cfg.SERVER_ADDRESS)
    server = HTTPServer(cfg.SERVER_ADDRESS, ReqHandler)
    print('Running server (type Ctrl+C to exit)...')
    print('\n### Logs ###\n')
    
    # Server run
    server.serve_forever()
    print('End')
except KeyboardInterrupt:
    server.shutdown()
    print('End')
