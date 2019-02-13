from http.server import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        def hello():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>Hello!</body></html>'
            self.wfile.write(output.encode())
            print(output)
            return
        try:
            if self.path.endswith('/hello'):
                hello()
            else:
                self.send_response(301)
                self.send_header('Location', webserverHandler)
                self.end_headers()
        except IOError:
            self.send_error(404, 'File Not Found %s', self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('Server running on port %s' % port)
        server.serve_forever()
    except KeyboardInterrupt as e:
        print('^C entered, stopping web server...')
        server.socket.close()

if __name__ == "__main__":
    main()