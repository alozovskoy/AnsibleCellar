#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import logging

import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient

import modulesCellar


class URIHandler(tornado.web.RequestHandler):

    def get(self, page):
        templVars = {}
        templVars['page'] = page
        if page == '/':
            page = 'index'
        try:
            if page.startswith('/inv'):
                if page.startswith('/inv/'):
                    templVars['data'] = modulesCellar.inv.getInvData(
                        '/' + page[5:])
                    self.render('templates/inv_file', **templVars)
                    return None
                else:
                    templVars['files'] = modulesCellar.inv.getInvs()
                    self.render(
                        'templates/' + page.split('/')[-1], **templVars)
                    return None
            if page.startswith('/playbook'):
                if page.startswith('/playbook/'):
                    playData = modulesCellar.playbook.getPlaybookData(
                        '/' + page[10:])
                    tags = []
                    for hosts in playData:
                        for task in playData[hosts]['tasks']:
                            for item in task[1].split(','):
                                tags.append(item.strip())
                    tags.sort()
                    tags = list(set(tags))
                    tags.sort()
                    templVars['tags'] = tags
                    templVars['data'] = playData
                    self.render('templates/playbook_file', **templVars)
                    return None
                else:
                    templVars['files'] = modulesCellar.playbook.getPlaybooks()
                    self.render(
                        'templates/' + page.split('/')[-1], **templVars)
                    return None

            templVars['content'] = 'test'
            self.render('templates/' + page.split('/')[-1], **templVars)
        except:
            self.set_status(404)
            self.render('templates/404', **templVars)

application = tornado.web.Application([
    (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': 'static/css/'}),
    (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': 'static/js/'}),
    (r'(.*)', URIHandler),
],
    debug=True,
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)-8s - %(message)s',
                    datefmt='%d/%m/%Y %Hh%Mm%Ss',
                    filename='cellar.log')
console = logging.StreamHandler(sys.stderr)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
