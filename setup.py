#!/usr/bin/env python3
"""Host a web server.

Web server implementing SQLAlchemy to demonstrate basic CRUD operations.
"""

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
        try:
            if self.path.endswith('/restaurant'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurants = session.query(Restaurant).all()
                output = '<html><body>'
                output += '<h4>'
                output += '<a href="/restaurant/new">Make a New Restaurant</a>'
                output += '</h4>'
                for restaurant in restaurants:
                    output += '''{} <a href="/restaurant/{}/edit">Edit</a> |
                                  <a href="/restaurant/{}/delete">Delete</a>'''\
                                      .format(restaurant.name, restaurant.id,
                                              restaurant.id)
                    output += '<br />'
                output += '</html></body>'
                session.close()

                self.wfile.write(output.encode())
                return
            elif self.path.endswith('/restaurant/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '<html><body>'
                output += '<h4>'
                output += '<a href="/restaurant">Back to restaurant list</a>'
                output += '</h4>'
                output += '''<form method = "POST" enctype =
                "multipart/form-data" action = "/restaurant/new"><h2>Enter new
                restaurant name: </h2><input name="newRestaurantName" type=
                "text"><input type="submit" value="Add"></form>'''
                output += '</html></body>'
                self.wfile.write(output.encode())
                return
            elif self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).\
                    filter_by(id=self.path.split('/')[2]).one()
                output = '<html><body>'
                output += '<h4>'
                output += '<a href="/restaurant">Back to restaurant list</a>'
                output += '</h4>'
                output += '<h3>'
                output += '{}'.format(restaurant.name)
                output += '</h3>'
                output += '''<form method="POST" enctype="multipart/form-data"
                action="edit"><h4>Edit restaurant name:</h4><input name=
                "restaurantName" type = "text"><input type = "submit"
                value = "Change"></form>'''
                output += '</html></body>'
                self.wfile.write(output.encode())
                session.close()
                return
            elif self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).\
                    filter_by(id=self.path.split('/')[2]).one()
                output = '<html><body>'
                output += '<h4>'
                output += '<a href="/restaurant">Back to restaurant list</a>'
                output += '</h4>'
                output += '<h3>'
                output += '{}'.format(restaurant.name)
                output += '</h3>'
                output += '''<form method="POST" enctype="multipart/form-data"
                action="delete"><h4>By pressing confirm this restaurant will be
                permanently removed from the database. </h4><button type=
                "submit" name="confirm" value="True">Confirm</button>'''
                output += '</html></body>'
                self.wfile.write(output.encode())
                session.close()
                return
            else:
                self.send_response(301)
                self.send_header('Location', '/restaurant')
                self.end_headers()
                return
        except IOError as e:
            self.send_error(404, 'File Not Found %s', self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurant/new'):
                c_type, p_dict = cgi.parse_header(
                    self.headers.get('Content-Type')
                )
                content_len = int(self.headers.get('Content-length'))
                p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
                p_dict['CONTENT-LENGTH'] = content_len
                message_content = ''
                if c_type == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, p_dict)
                    message_content = fields.get('newRestaurantName')
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                new_restaurant = Restaurant(name=message_content[0].decode())
                session.add(new_restaurant)
                session.commit()
                session.close()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()
                return
            elif self.path.endswith('/edit'):
                c_type, p_dict = cgi.parse_header(
                    self.headers.get('Content-Type')
                )
                content_len = int(self.headers.get('Content-length'))
                p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
                p_dict['CONTENT-LENGTH'] = content_len
                message_content = ''
                if c_type == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, p_dict)
                    new_name = fields.get('restaurantName')
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).\
                    filter_by(id=self.path.split('/')[2]).one()
                restaurant.name = new_name[0].decode()
                session.add(restaurant)
                session.commit()
                session.close()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()
            elif self.path.endswith('/delete'):
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).\
                    filter_by(id=self.path.split('/')[2]).one()
                session.delete(restaurant)
                session.commit()
                session.close()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()
            else:
                self.send_response(301)
                self.send_header('Location', '/')
                self.end_headers()
                return
        except IOError as e:
            self.send_error(404, 'File Not Found %s', self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('0.0.0.0', port), webserverHandler)
        print('Server running on port %s' % port)
        server.serve_forever()
    except KeyboardInterrupt as e:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == "__main__":
    main()
