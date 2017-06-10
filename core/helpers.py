#!/usr/bin/env python2

import variables

import os
import yaml


def terraform_configs_yaml_array(file_name, array_name):
    array_string=""
    for key, value in yaml.load(open(variables.cwd + '/terraform/configs/{}.yaml'.format(file_name)))[array_name].iteritems():
        array_string+='-var \'{}={}\' '.format(key, value)
    return array_string
