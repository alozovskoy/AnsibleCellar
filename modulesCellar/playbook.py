#!/usr/bin/env python

import os

import configparser
import yaml

from collections import OrderedDict

config = configparser.ConfigParser()
config.read(os.getcwd().replace('modulesCellar', '') + '/cellar.conf')
playbooksPath = config['Environment']['playbooksPath']


def getPlaybooks():
    playbooks = []
    for d in os.walk(playbooksPath):
        if not d[1]:
            for item in d[2]:
                playbooks.append([d[0].replace(playbooksPath, ''), item])
    return playbooks


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def getPlaybookData(playbook):
    playFile = open(playbooksPath + '/' + playbook)
    yfile = ordered_load(playFile)
    data = {}
    for item in yfile:

        data[item['hosts']] = {}
        data[item['hosts']]['name'] = item.get('name', 'noname')
        data[item['hosts']]['tasks'] = []
        for task in item['tasks']:
            try:
                name = task['name']
            except:
                name = task.keys()[0] + ': ' + task.itervalues().next()
            tags = task.get('tags', 'notags')
            data[item['hosts']]['tasks'].append(
                [name, ', '.join(tags) if isinstance(tags, list) else tags])

    return data
