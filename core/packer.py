#!/usr/bin/env python2

import variables
import helpers

import os
import yaml
import boto3
import sys

from fabric.api import abort, task, puts, roles, local, env, lcd
from fabric import state
from fabric.task_utils import crawl


def install_packer():
    local("wget -O /tmp/packer.zip " + variables.packer_url)
    local("sudo unzip -o /tmp/packer.zip -d /opt/packer")
    value = str("export PATH=$PATH:/opt/packer")
    with open(os.environ['VIRTUAL_ENV'] + '/bin/postactivate', 'a+') as f:
        if not any(value == x.rstrip('\r\n') for x in f):
            f.write(value + '\n')
