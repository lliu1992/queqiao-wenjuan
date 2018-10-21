
import os

import tornado.ioloop
import urls


def get_template_dir():
    pwd = os.getcwd()
    return os.path.join(pwd, 'templates')


app_template_path = get_template_dir()


if __name__ == '__main__':
    print('======wj_deploy started=====')
    application = urls.make_app()
    application.settings = {
        'template_path': app_template_path,
    }

    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()