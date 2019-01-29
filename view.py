#coding=utf-8


import subprocess

import base
import config
import utils


class TestHandler(base.BaseHandler):

    def get(self):
        self.write('hello world')


class IndexHandler(base.BaseHandler):

    def get(self):
        self.render('index.html', )


class GetdomainDataHandler(base.BaseHandler):
    def get(self):
        domain_info_list = []

        domain_list = config.DOMAIN_LIST
        for domain in domain_list:
            branch = utils.get_branch_on_domain(domain)
            update_time = utils.get_branch_updatetime_on_domain(domain)
            domain_info_list.append(dict(domain=domain, branch=branch, update_time=update_time))

        self.write(dict(status=200, status_code=1, data=domain_info_list))


class UpdateAndDeployHandler(base.BaseHandler):
    @utils.auth_params
    def post(self):
        domain = self.get_argument('domain','')
        status_code = 0
        cwd = utils.get_cwd(domain)
        stp_p = subprocess.Popen('sh startup.sh', shell=True, stdout=subprocess.PIPE, cwd=cwd)

        if 'success' not in stp_p.stdout.read():
            self.write(dict(status=200, status_code=status_code))
            return
        
        status_code = 1
        utils.set_branch_updatetime_on_domain(domain)
        update_time = utils.get_branch_updatetime_on_domain(domain)
        data = {'update_time': update_time}
        
        self.write(dict(status=200, status_code=status_code, data=data))


class ExcuteInitScript(base.BaseHandler):
    @utils.auth_params
    def post(self):
        domain = self.get_argument('domain', '')
        excute_script = self.get_argument('excute_script', '')

        status_code = 0

        if not excute_script:
            self.write(dict(status=200, status_code=status_code))
            return

        cwd = utils.get_cwd(domain)
        if excute_script:
            stp_p = subprocess.Popen('init_script.py', shell=True, stdout=subprocess.PIPE, cwd=cwd)
            if 'success' in stp_p.stdout.read():
                status_code = 1

        self.write(dict(status=200, status_code=status_code))


class CheckoutBranchAndDeploy(base.BaseHandler):

    @utils.auth_params
    def post(self):
        domain = self.get_argument('domain', '')
        branch = self.get_argument('branch', '')

        current_branch = utils.check_out_branch(domain, branch)
        if current_branch != branch:
            self.write(dict(status=200, status_code=0, err_msg=u'切换分支失败，请检查分支是否存在'))
            return 
            
        stp_p = subprocess.Popen('sh startup.sh', shell=True, stdout=subprocess.PIPE, cwd=cwd)

        if current_branch == branch and 'sucess' in stp_p.stdout.read():
            utils.set_branch_updatetime_on_domain(domain)
            update_time = utils.get_branch_updatetime_on_domain(domain)
            self.write(dict(status=200, status_code=1, data=dict(branch=current_branch, update_time=update_time)))

        else:
            self.write(dict(status=200, status_code=0, err_msg=u'操作有误'))


class GetCurrentBranchHandler(base.BaseHandler):

    @utils.auth_params
    def get(self):
        domain = self.get_argument('domain', '')

        current_branch = utils.get_cur_branch_on_domain(domain)
        data = dict(branch=current_branch)
        self.write(dict(status=200, status_code=0, data=data))