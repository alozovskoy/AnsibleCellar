#!/usr/bin/env python

import os

import configparser

config = configparser.ConfigParser()
config.read(os.getcwd().replace('modulesCellar', '') + '/cellar.conf')
invPath = config['Environment']['invsPath']


def parseVars(config, groupName):
    variables = ''
    for var in config[groupName + ':vars'].items():
        for v in var:
            if v:
                variables += v + ' '
    vardata = dict(var.split('=')
                   for var in filter(None, variables.replace(' = ', '=').split(' ')))
    return vardata


def getInvs():
    invs = []
    for d in os.walk(invPath):
        if not d[1]:
            substr = ['group_vars', 'host_vars', '.svn', '.git', '.cellar']
            if not any([i in d[0] for i in substr]):
                    for item in d[2]:
                            if 'hosts' == item:
                                invs.append(
                                    d[0].replace(invPath, '').rsplit('/', 1))
                            else:
                                invs.append([d[0].replace(invPath, ''), item])
    return invs


def getInvData(inventory):
    data = {}
    config = configparser.ConfigParser(
        allow_no_value=True, delimiters=(' '), strict=False)
    if inventory[0] == '/':
        inventory = inventory[1:]
    inventory = os.path.join(invPath, inventory)
    if os.path.isfile(inventory):
        config.read(inventory)
    else:
        config.read(os.path.join(inventory, 'hosts'))
    keysdict = {}
    keysdict['groups'] = []
    keysdict['vars'] = []
    keysdict['childrens'] = []
    for item in config.sections():
        if item.endswith(':vars'):
            keysdict['vars'].append(item.replace(':vars', ''))
        elif item.endswith(':children'):
            keysdict['childrens'].append(item.replace(':children', ''))
        else:
            keysdict['groups'].append(item)

    for item in keysdict['groups']:
        data[item] = {}
        for host in config[item]:
            data[item][host] = {}
            if config[item][host]:
                data[item][host] = dict(var.split('=')
                                        for var in config[item][host].split(' '))

    while keysdict['childrens']:
        for item in keysdict['childrens']:
            children = config[item + ':children']
            if set(config[item + ':children']).issubset(set(data)):
                data[item] = {}
                for i in children:
                    for ii in data[i]:
                        data[item][ii] = data[i][ii]
                keysdict['childrens'].remove(item)
    for item in keysdict['vars']:
        if item in keysdict['groups']:
            pass
        if item in keysdict['childrens']:
            pass
        if item == 'all':
            pass
    return data
