# -*- coding: utf-8 -*-

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

import json

import src.db_manager as mng
import src.config as cfg


class ReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global SERVER_DATA, OSC, CHANNELS, SEQNAME, METADATA, ITER_TOKEN, q
        path_str = urlparse(self.path)
        path = path_str.path
        queryRaw = parse_qs(path_str.query)
        query = {}
        for key, value in queryRaw.items():
            query[key] = value[0]
        
        if path == '/test':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            self.wfile.write(bytes("OK", "utf8"))
            print('test')

        # Data insert
        elif path == "/data":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            tab_name = query.pop('tab_name')
            mng.insert_data(
                tab_name,
                query
            )

        # DB management
        elif path == "/get_db_tree":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()

            db_tree = json.dumps(mng.get_db_tree())
            self.wfile.write(bytes(db_tree, "utf-8"))

        elif path == "/add_table":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # print(query['tab_name'])
            # print(json.loads(query['col_settings']))
            try:
                try:
                    sensor = int(query['sensor'])
                except KeyError:
                    sensor = True
            
                mng.add_table(
                    query['tab_name'],
                    json.loads(query['col_settings']),
                    sensor=sensor
                )
            except KeyError as e:
                print("Adding new table failed!", e)

        elif path == "/add_column":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # print(query['tab_name'])
            # print(json.loads(query['col_settings']))
            try:
                mng.add_columns(
                    query['tab_name'],
                    json.loads(query['col_settings'])
                )
            except KeyError as e:
                print("Adding new column failed!", e)

        elif path == "/remove_table":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # print(query['tab_name'])
            # print(json.loads(query['col_settings']))
            try:
                mng.remove_table(
                    query['tab_name']
                )
            except KeyError as e:
                print("Removing table failed!", e)

        elif path == "/remove_column":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # print(query['tab_name'])
            # print(json.loads(query['col_settings']))
            try:
                mng.remove_column(
                    query['tab_name'],
                    query['col_name']
                )
            except KeyError as e:
                print("Removing column failed!", e)

        # Show website
        elif path == '/home' or path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            with open('./site/site.html', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        # File imports
        elif path == '/style/style.css':
            self.send_response(200)
            self.send_header('Content-type','text/css')
            self.end_headers()

            with open('./site/style/style.css', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/src/tabs.js':
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()

            with open('./site/src/tabs.js', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/src/db_management.js':
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()

            with open('./site/src/db_management.js', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/src/json-view.js':
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()

            with open('./site/src/json-view.js', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/style/jsonview.css':
            self.send_response(200)
            self.send_header('Content-type','text/css')
            self.end_headers()

            with open('./site/style/jsonview.css', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/src/utils/getDataType.js':
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()

            with open('./site/src/utils/getDataType.js', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        elif path == '/src/utils/dom.js':
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()

            with open('./site/src/utils/dom.js', 'r') as f:
                self.wfile.write(bytes(f.read(), 'utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()

