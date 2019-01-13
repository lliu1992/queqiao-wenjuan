# coding=utf-8

import os

import subprocess
import functools

import config


def get_cur_branch_on_domain(domain):
    cwd = get_cwd(domain)
    p = subprocess.Popen('git branch', shell=True, stdout=subprocess.PIPE, cwd=cwd)
    branches_str = p.stdout.read()
    cur_branch = get_cur_branch(branches_str)
    return cur_branch


def get_cwd(domain):
    domain_dir_name = config.DOMAIN_DIR_MAP.get(domain)
    pwd = os.getcwd()
    parant_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    return os.path.join(parant_path, domain_dir_name)


def get_cur_branch(branches_str):
    branch_list = branches_str.split('\n')
    for br in branch_list:
        if br.startswith('*'):
            return br.replace('*', '').strip()


def check_out_branch(domain, branch):
    """

    :param domain:  domain
    :param branch:  the branch you want to checkout
    :return: current branch after excute git checkout branch which is specified
    """
    cwd = get_cwd(domain)
    subprocess.call('git checkout .', shell=True, cwd=cwd)
    subprocess.call('git pull', shell=True, stdout=subprocess.PIPE, cwd=cwd)
    if domain in ['wxtest01', 'wj_app_api']:
        subprocess.call('cp -f openapi/config.py_bak openapi/config.py', shell=True, cwd=cwd)
    subprocess.call('git checkout {0}'.format(branch), shell=True, stdout=subprocess.PIPE, cwd=cwd)

    return get_cur_branch_on_domain(domain)


def auth_params(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        domain = self.get_argument('domain', '')

        if not domain:
            self.write(dict(status=200, status_code=0, err_msg=u'请输入域名'))
            return
        return method(self, *args, **kwargs)

    return wrapper





