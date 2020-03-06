#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: davabrams
"""

# RUN THIS TO START THE GAME SERVER!
#the server will run in the background (ctrl-c to end)

#this is the http server
# 'borrowed' from https://www.afternerd.com/blog/python-http-server/
# and from https://stackabuse.com/using-curl-in-python-with-pycurl/
# and from https://stackoverflow.com/questions/31826814/curl-post-request-into-pycurl-code
import json
from io import BytesIO 
from tileGameServerSettings import PORT, ip
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from tileGameAlgo import solvePuzzleSimple
from tileGameAlgo import solvePuzzleVerbose

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    #structure stolen off the web, but do_POST gut-reno'd
    def do_GET(self):
       self.send_error(666, 'we dont do no GET around here BEN')

    def do_POST(self):
        try:
            self.send_response(200)
            self.end_headers()
            datalen = int(self.headers['Content-Length'])
            message = json.loads(self.rfile.read(datalen))
            userState = message['puzzle_values'] #this is the state of the puzzle parsed from the POST data
            if (False == message['verbose']):
                result = solvePuzzleSimple(userState) #comes back as a string
            else:
                result = solvePuzzleVerbose(userState) #comes back as a string
            self.wfile.write(bytes(result, encoding='utf-8'))
        except:
            self.send_error(666, 'unknown error BEN')

httpd = HTTPServer((ip, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()