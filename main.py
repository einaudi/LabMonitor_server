# -*- coding: utf-8 -*-

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

import json
import requests

import db_manager as mng
import config as cfg


class ReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global SERVER_DATA, OSC, CHANNELS, SEQNAME, METADATA, ITER_TOKEN, q
        path_str = urlparse(self.path)
        path = path_str.path
        queryRaw = parse_qs(path_str.query)
        query = {}
        for key, value in queryRaw.items():
            query[key] = value[0]

        # needed by handler
        if path == '/test':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes("OK", "utf8"))
            print('test')

        elif path == "/data":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            tab_name = query.pop('tab_name')
            mng.insert_data(
                tab_name,
                query
            )

        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()

try:
    print('Starting server on %s:%i...' % cfg.SERVER_ADDRESS)
    server = HTTPServer(cfg.SERVER_ADDRESS, ReqHandler)
    print('Running server (type Ctrl+C to exit)...')
    print('\n### Logs ###\n')
    server.serve_forever()
    print('End')
except KeyboardInterrupt:
    server.shutdown()
    print('End')
