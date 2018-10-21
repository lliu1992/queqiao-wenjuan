
import os

import tornado.web
import view

def make_app():
    return tornado.web.Application([
        (r'/test/', view.TestHandler),
        (r'/', view.IndexHandler),

    ])
