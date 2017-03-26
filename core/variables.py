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
cwd = os.getcwd()
