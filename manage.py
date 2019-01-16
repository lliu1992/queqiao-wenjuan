#coding=utf-8

import os

import tornado.httpserver
import tornado.ioloop

import urls

app_settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),

}


if __name__ == '__main__':

    print('======wj_deploy started=====')
    application = urls.make_app()
    application.settings = app_settings

    server = tornado.httpserver.HTTPServer(application)
    server.bind(9900)
    server.start(2)     # multipul process 2.
    tornado.ioloop.IOLoop.instance().start()