import json
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

from method_server import run_method
server_running = True

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/exit':
            global server_running
            server_running = False
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'GET request received for root path'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            response = {'message': 'not fond', 'code': 404}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = run_method(data)
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            response = {'message': 'not fond', 'code': 404}
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=9630):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    while server_running:
        httpd.handle_request()


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(run)
