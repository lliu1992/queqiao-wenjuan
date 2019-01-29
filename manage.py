#coding=utf-8

import os

import tornado.httpserver
import tornado.ioloop

import urls
import config


def main():
    print('======wj_deploy started=====')
    application = urls.make_app()
    application.settings = config.app_settings
    server = tornado.httpserver.HTTPServer(application)
    server.bind(9800)
    server.start(1)  # multipul process 2.
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

