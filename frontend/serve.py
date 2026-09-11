import http.server
import socketserver
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


class Server(socketserver.TCPServer):
    allow_reuse_address = True


port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
with Server(('127.0.0.1', port), NoCacheHandler) as httpd:
    print(f'Serving frontend on http://127.0.0.1:{port} (no-cache)')
    httpd.serve_forever()