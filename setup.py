from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi
import cgitb
cgitb.enable()

from db_setup import Base, Restaurant, MenuItem


class webserverHandler(BaseHTTPRequestHandler):
    """Fetch definition of http method."""
    def do_GET(self):
        """Run http GET request."""
        def hello():
            """Present hello.html."""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ''
            output += '<html><body>Hello!</body></html>'
            output += '''<form method = "POST" enctype = "multipart/form-data"
            action = "hello"><h2>What would you like me to say?</h2><input name
             = "message" type = "text"><input type = "submit" value = "Submit">
             </form>'''
            self.wfile.write(output.encode())
            print(output)
            return

        def hola():
            """Present hola.html."""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '''<html><body>Hola <a href="/hello">Back to Hello</a>
            </body></html>'''
            output += '''<form method = "POST" enctype = "multipart/form-data"
            action = "hello"><h2>What would you like me to say?</h2><input name
             = "message" type = "text"><input type = "submit" value = "Submit">
             </form>'''
            self.wfile.write(output.encode())
            print(output)
            return
        try:
            if self.path.endswith('/hello'):
                hello()
                return
            if self.path.endswith('/hola'):
                hola()
                return
            if self.path.endswith('/restaurant'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurants = session.query(Restaurant).all()
                output = '<h1>'
                for restaurant in restaurants:
                    output += '{}   <a href="#">Edit</a> | \
                                  <a href="#">Delete</a>'.format(restaurant.name)
                    output += '<br />'
                output += '</h1>'
                session.close()

                self.wfile.write(output.encode())
                return
            if self.path.endswith('/'):
                self.send_response(301)
                self.send_header('Location', '/hello')#webserverHandler)
                self.end_headers()
                return
        except IOError as e:
            self.send_error(404, 'File Not Found %s', self.path)
    def do_POST(self):
        if self.path.endswith('/'):
            try:
                self.send_response(200)
                self.end_headers()
                c_type, p_dict = cgi.parse_header(self.headers.get('Content-Type'))
                content_len = int(self.headers.get('Content-length'))
                p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
                p_dict['CONTENT-LENGTH'] = content_len
                message_content = ''
                if c_type == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, p_dict)
                    message_content = fields.get('message')
                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: </h2>'
                output += '<h1>{}</h1>'.format(message_content[0].decode())
                output += '''<form method = "POST" enctype = "multipart/form-data"
                action = "hello"><h2>What would you like me to say?</h2><input name
                = "message" type = "text"><input type = "submit" value = "Submit">
                </form>'''
                output += '</html></body>'
                self.wfile.write(output.encode())
            except IOError as e:
                self.send_error(404, 'File Not Found %s', self.path)
        if self.path.endswith('/restaurant'):
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                db = session.query(Restaurant).filter_by().all()
                output = '<h1>'
                for entry in db:
                    output += '{}'.format(entry.name)
                    output += '<br />'
                output += '</h1>'
                session.close()

                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: </h2>'
                output += '<h1>{}</h1>'.format(message_content[0].decode())
                output += '''<form method = "POST" enctype = "multipart/form-data"
                action = "hello"><h2>What would you like me to say?</h2><input name
                = "message" type = "text"><input type = "submit" value = "Submit">
                </form>'''
                output += '</html></body>'
            except IOError as e:
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
