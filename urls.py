#coding=utf-8

import os

import tornado.web
import view

def make_app():
    return tornado.web.Application([
        (r'/test/?', view.TestHandler),
        (r'/?', view.IndexHandler),
        (r'/upload_and_deploy/?', view.UpdateAndDeployHandler),
        (r'/checkout_and_deploy/?', view.CheckoutBranchAndDeploy),
        (r'/get_current_branch/?', view.GetCurrentBranchHandler),

    ])
