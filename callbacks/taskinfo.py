#!/usr/bin/python

import os
import sqlite3

task_id = os.environ['ANSIBLE_TASK_ID']


class CallbackModule(object):

    def playbook_on_play_start(self, pattern):
        con = sqlite3.connect('/home/ansible/ansible.db', 10.0)
        cur = con.cursor()
        cur.execute('update tasks set ppid = ?, playbook = ?, inventory = ?, vars = ?, tags = ?, skipped_tags = ? where id = ?', (
            os.getpid(),
            self.playbook.filename,
            self.playbook.inventory.src(),
            str(self.playbook.extra_vars),
            ', '.join(self.playbook.only_tags),
            ', '.join(self.playbook.skip_tags),
            task_id))
        con.commit()
        con.close()

    def playbook_on_stats(self, stats):
        statsNames = {'ok': 'ok', 'changed': 'changed', 'skipped':
                      'skipped', 'dark': 'unreachable', 'failures': 'failed'}
        status = 'unknown'
        for item in ['ok', 'changed', 'skipped', 'dark', 'failures']:
            if len(getattr(stats, item)):
                status = statsNames[item]
        con = sqlite3.connect('/home/ansible/ansible.db', 10.0)
        cur = con.cursor()
        cur.execute(
            'update tasks set status = ? where id = ? ', (status, task_id))
        con.commit()
        con.close()
