#!/usr/bin/env python

import os
import sys
import json
import time

import sqlite3

task_id = os.environ['ANSIBLE_TASK_ID']

stepName = ''
stepStart = ''
stepNumber = 0


def insertData(host, data, status):
    con = sqlite3.connect('/home/ansible/ansible.db', 10.0)
    cur = con.cursor()
    cur.execute('insert into steps ("taskid", "stepNumber", "stepName", "start", "stop", "hostname", "data", "status") values (?, ?, ?, ?, ?, ?, ?, ?)', (
        task_id,
        stepNumber,
        str(stepName),
        stepStart,
        int(time.time()),
        host,
        str(data),
        status
    ))
    con.commit()
    con.close()


class CallbackModule(object):

    def on_any(self, *args, **kwargs):
        if hasattr(self, 'task') and hasattr(self.task, 'name'):
            if args[0] == self.task.name:
                    global stepStart
                    global stepName
                    global stepNumber
                    stepStart = int(time.time())
                    stepName = self.task.name
                    stepNumber += 1

    def runner_on_failed(self, host, res, ignore_errors=False):
        status = 'failed'
        insertData(host, res, status)

    def runner_on_ok(self, host, res):
        if 'changed' in res.keys() and res['changed']:
            status = 'changed'
        else:
            status = 'ok'
        insertData(host, res, status)

    def runner_on_skipped(self, host, item):
        res = str(self.task.when)
        status = 'skipped'
        insertData(host, res, status)

    def runner_on_unreachable(self, host, res):
        status = 'unreachable'
        insertData(host, res, status)

    def runner_on_no_hosts(self):
        host = 'none'
        res = 'no hosts'
        status = 'nohosts'
        insertData(host, res, status)
