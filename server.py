#!/usr/bin/env python3

# Example HTTP server
#
# See <https://docs.python.org/3/library/http.server.html> for details
#

import http.server
import socketserver
import redact
import json

PORT = 8080


class ExampleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Call MOAAS and PurgoMalum APIs by calling redact.py
        response = redact.main(self.path)
        response = json.loads(response)
        message = response['message']
        subtitle = response['subtitle']
        
        # Return censored HTML document
        payload = (
            f'<!DOCTYPE html>'
            f'<html> <head> <title>'
            f'FOAAS - {message} {subtitle}'
            f'</title>'
            f'<meta charset="utf-8">'
            f'<meta property="og:title" content="{message} {subtitle}>'
            f'<meta property="og:description" content="{message} {subtitle}">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">'
            #f'<script>   window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-143325008-1'); </script>'
            f'</head> <body style="margin-top:40px;">'

            f'<div class="container"> <div id="view-10">'
            f'<div class="hero-unit">'
            f'<h1>{message}</h1>'
            f'<p><em>{subtitle}</em></p> </div> </div> <p style="text-align: center"><a href="https://foaas.com">foaas.com</a></p>'
            f'</div> </body> </html>'
        )

        self.wfile.write(payload.encode('utf-8'))


with socketserver.TCPServer(("", PORT), ExampleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
