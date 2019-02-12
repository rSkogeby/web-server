from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('\hello'):
                pass
        except KeyboardInterrupt as e:
            print('Error: ',)


def main():
    port = 8080
    server = HTTPServer(('', port), webserverHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()