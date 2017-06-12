#!/usr/bin/env python2

import variables

import os
import yaml


def terraform_configs_yaml_list(file_name):
    list_string=""
    configs_array=yaml.load(open(variables.cwd + '/terraform/configs/{}.yaml'.format(file_name))).keys()
    for section in configs_array:
        section_array=[]
        list_string+='-var \'{}={{'.format(section)
        for key, value in yaml.load(open(variables.cwd + '/terraform/configs/{}.yaml'.format(file_name)))[section].iteritems():
            section_array.append('{}=\"{}\"'.format(key, value))
        list_string+=",".join(section_array)
        list_string+='}\' '
    return list_string
