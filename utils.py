#coding=utf-8


import os
import subprocess
import functools
import time


import redis

import config


pool = redis.ConnectionPool(
    host=config.REDIS_HOST, port=config.REDIS_PORT
)


def get_redis_conn():
    return redis.Redis(connection_pool=pool)

redis_client = get_redis_conn()


def get_branch_on_domain(domain):
    branch = redis_client.get(domain)
    if not branch:
        branch = get_cur_branch_on_domain(domain)
    
    return branch

        
def get_cur_branch_on_domain(domain):
    cwd = get_cwd(domain)
    p = subprocess.Popen('git branch', shell=True, stdout=subprocess.PIPE, cwd=cwd)
    branches_str = p.stdout.read()
    cur_branch = get_cur_branch(branches_str)
    
    return cur_branch



def get_branch_updatetime_on_domain(domain):
    key = '{0}_{1}'.format(domain, 'update')
    update_time = redis_client.get(key)
    
    if not update_time:
        update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
    return update_time


def set_branch_updatetime_on_domain(domain):
    key = '{0}_{1}'.format(domain, 'update')
    update_time = time.strftime("%Y-%m-%d %H:%M:%S")

    redis_client.set(key, update_time)



def get_cwd(domain):
    domain_dir_name = config.DOMAIN_DIR_MAP.get(domain)
    pwd = os.getcwd()
    parant_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    print 'parant_path:', parant_path
    print 'domain_dir_name:', domain_dir_name
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
    subprocess.call('git checkout master', shell=True, cwd=cwd)
    subprocess.call('git pull', shell=True, stdout=subprocess.PIPE, cwd=cwd)
    subprocess.call('git checkout {0}'.format(branch), shell=True, stdout=subprocess.PIPE, cwd=cwd)
    branch =  get_cur_branch_on_domain(domain)
    set_branch_on_domain(domain, branch)

    return branch


def set_branch_on_domain(domain, branch):
    redis_client.set(domain, branch)


def auth_params(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        domain = self.get_argument('domain', '')

        if not domain:
            self.write(dict(status=200, status_code=0, err_msg=u'请输入域名'))
            return
        return method(self, *args, **kwargs)

    return wrapper





