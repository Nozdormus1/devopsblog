#!/usr/bin/env python2

import yaml
import os

with open('global.yaml', 'r') as f:
    globals_yaml = yaml.load(f)

region = globals_yaml['region']
aws_profile = globals_yaml['aws_profile']
profiles = globals_yaml['profiles']
states_bucket = globals_yaml['states_bucket']
terraform_url = globals_yaml['terraform_url']
packer_url = globals_yaml['packer_url']
cwd = os.getcwd()

def environment():
    with open('.environment', 'r') as env_file:
        return env_file.read()
