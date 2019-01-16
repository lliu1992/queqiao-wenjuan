#coding=utf-8

DOMAIN_LIST = ['wxtest01', 'mini_app', 'ios1', 'android1', 'm-wenjuan']

DOMAIN_DIR_MAP = {
    'wxtest01': 'wxtest01',
    'mini_app': 'wj_mini_app',
    'ios1': 'wj_app_api',
    'android1': 'wj_android',
    'm-wenjuan': 'm-wenjuan-xt',
    't1': 'wj_t1',
    't2': 'wj_t2',

}


REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'


TEST_ENV = True

if TEST_ENV:
    DOMAIN_LIST = ['wenjuan']
    DOMAIN_DIR_MAP = {'wenjuan': 'wenjuan'}

