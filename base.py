#coding=utf-8

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def check_xsrf_token(self):
        return
