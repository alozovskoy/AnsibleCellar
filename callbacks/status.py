#!/usr/bin/env python

import os
import sqlite3


task_id = os.environ['ANSIBLE_TASK_ID']

con = sqlite3.connect('/home/ansible/ansible.db')
cur = con.cursor()


def set_rc(rc):
    cur.execute('update tasks set "rc" = ' + rc + ' where id = ' + task_id)
    con.commit()


class CallbackModule(object):

    def playbook_on_play_start(self, pattern):
        cur.execute('update tasks set ppid = ?, playbook = ?, inventory = ?, vars = ? where id = ?', (
            str(os.getpid()),
            str(self.playbook.filename),
            str(self.playbook.inventory.src()),
            str(self.playbook.extra_vars),
            task_id))
        con.commit()

    def playbook_on_no_hosts_matched(self):
        set_rc('4')

    def runner_on_no_hosts(self):
        set_rc('5')

    def playbook_on_no_hosts_remaining(self):
        set_rc('6')
