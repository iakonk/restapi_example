import json
import argparse
import yaml
import logging
import os
import signal

import txtemplate

from twisted.internet import reactor
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

from restapi_project.pools import create_pool
from restapi_project import init_logging
from restapi_project.db_actions import insert_action, select_action


POOL_SIZE = 2
TEMPLATE_DIR = os.path.join('restapi_project', "templates")


class AppUserRegForm(Resource):
    isLeaf = True

    def __init__(self, cfg):
        self.log = logging.getLogger(self.__class__.__name__)
        self.table = cfg['database']['table']
        self.db_filename = cfg['database']['filename']
        self.db_pool = create_pool(POOL_SIZE, self.db_filename)
        self.loader = txtemplate.Jinja2TemplateLoader(TEMPLATE_DIR)

        self.select_action = select_action.SelectAllAction(self.db_pool,
                                                           self.table,
                                                           ('id','f_name','l_name','email','phone','primary_skill'))
        self.insert_action = insert_action.InsertAction(self.db_pool,
                                                        self.table,
                                                        ('f_name', 'l_name', 'email', 'phone', 'primary_skill'))

    def write_response(self, content, request):
        request.write(content)
        request.setResponseCode(200)
        request.finish()

    def write_json_data(self, content, request):
        request.write(json.dumps(content))
        request.setResponseCode(200)
        request.finish()

    def get_all_registrations(self, data, request):
        template_name = "all_registrations.html"
        template = self.loader.load(template_name)
        d = template.render(records_list=data)
        d.addCallback(self.write_json_data, request)

    def register(self, request):
        template_name = "register.html"
        template = self.loader.load(template_name)
        context = {"greeting": "Hello"}
        d = template.render(**context)
        d.addCallback(self.write_response, request)

    def render_home_page(self, request):
        template_name = "home.html"
        template = self.loader.load(template_name)
        context = {"home": "home page"}
        d = template.render(**context)
        d.addCallback(self.write_response, request)

    def render_GET(self, request):
        if request.postpath[0] == 'all_registrations':
            res = self.select_action()
            res.addCallback(self.get_all_registrations, request)
        elif request.postpath[0] == 'register':
            self.register(request)
        else:
            self.render_home_page(request)
        return NOT_DONE_YET

    def get_registration_result(self, data, request):
        template_name = "registration_result.html"
        template = self.loader.load(template_name)
        context = {"home": "home page"}
        d = template.render(**context)
        d.addCallback(self.write_response, request)

    def render_POST(self, request):
        self.log.debug(request.__dict__)
        res = self.insert_action(f_name=request.args['f_name'][0],
                                 l_name=request.args['l_name'][0],
                                 email=request.args['email'][0],
                                 phone=request.args['phone'][0],
                                 primary_skill=request.args['primary_skill'][0])
        res.addCallback(self.get_registration_result, request)
        return NOT_DONE_YET


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='append_const', const=1)
    parser.add_argument('-l', '--logdir', default='./', required=False)
    parser.add_argument('-c', '--config', nargs='?', type=argparse.FileType('r'), default='etc/config.yml')
    args = parser.parse_args()
    config = yaml.safe_load(args.config)
    init_logging(args)
    try:
        resource = AppUserRegForm(config)
        factory = Site(resource)
        reactor.listenTCP(8880, factory)
        reactor.run()
    finally:
        os.kill(0, signal.SIGKILL)