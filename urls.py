#coding=utf-8

import os

import tornado.web

import view
import config


def make_app():
    return tornado.web.Application([
        (r'/test/?', view.TestHandler),
        (r'/?', view.IndexHandler),
        (r'/get_domain_data/?', view.GetdomainDataHandler),
        (r'/upload_and_deploy/?', view.UpdateAndDeployHandler),
        (r'/checkout_and_deploy/?', view.CheckoutBranchAndDeploy),
        (r'/get_current_branch/?', view.GetCurrentBranchHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": config.app_settings.get('static_path')}),

    ])

