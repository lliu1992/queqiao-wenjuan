
import subprocess

import base
import config
import utils


class TestHandler(base.BaseHandler):

    def get(self):
        self.write('hello world')


class IndexHandler(base.BaseHandler):

    def get(self):
        domain_list = config.DOMAIN_LIST
        self.render('index.html', domain_list=domain_list)


class GetCurrentBranchHandler(base.BaseHandler):

    @utils.auth_params
    def get(self):
        domain = self.get_argument('domain', '')

        current_branch = utils.get_cur_branch_on_domain(domain)
        data = dict(current_branch=current_branch)
        self.write(dict(status=200, status_code=0, data=data))


class CheckOutBranchOnDomain(base.BaseHandler):

    @utils.auth_params
    def post(self):
        domain = self.get_argument('domain', '')
        branch = self.get_argument('branch', '')

        current_branch = utils.check_out_branch(domain, branch)

        if current_branch == branch:
            self.write(dict(status=200, status_code=1, data=dict(current_branch=current_branch)))

        else:
            self.write(dict(status=200, status_code=0, err_msg=u'操作有误'))


class UpdateAndDeployHandler(base.BaseHandler):

    @utils.auth_params
    def post(self):
        domain = self.get_argument('domain','')
        script_num = self.get_argument('script', '')

        status_code = 0
        cwd = utils.get_cwd(domain)
        stp_p = subprocess.Popen('sh startup.sh', shell=True, stdout=subprocess.PIPE, cwd=cwd)

        if script_num:
            script = config.SCRIPT_NUM_MAP.get(script_num)
            subprocess.call(script, shell=True, cwd=cwd)

        if 'sucess' in stp_p.stdout.read():
            status_code = 1

        self.write(dict(status=200, status_code=status_code))
