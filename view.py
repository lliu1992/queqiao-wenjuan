
import base
import config


class TestHandler(base.BaseHandler):
    def get(self):
        self.write('hello world')


class IndexHandler(base.BaseHandler):
    def get(self):
        domain_list = config.DOMAIN_LIST
        self.render('index.html', domain_list=domain_list)


class DeployHandler(base.BaseHandler):
    def post(self):
        domain = self.get_argument('domain','')
        branch = self.get_argument('branch', '')

        pass


