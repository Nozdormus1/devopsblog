#!/usr/bin/env python2

import variables
import terraform

import os
import yaml

from fabric.api import abort, task, puts, roles, local, env, lcd
from fabric import state
from fabric.task_utils import crawl


@task
def configure_aws_credentials():
    access_key = raw_input("Enter your aws access key: ")
    secret_key = raw_input("Enter your aws secret key: ")

    local("mkdir -p ~/.aws")
    credentials = '[{}]'.format(variables.aws_profile) + '\naws_access_key_id = {}'.format(access_key) \
                  + '\naws_secret_access_key = {}'.format(secret_key)
    local('test -f ~/.aws/credentials && mv ~/.aws/credentials ~/.aws/credentials.bac || touch ~/.aws/credentials')
    local('echo \"' + credentials + '\" > ~/.aws/credentials')


@task
def change_env(username, environment):
    try:
        file = open('.environment', 'r')
    except IOError:
        file = open('.environment', 'w')
    file.close()
    file = open('.environment', 'w')
    file.write(environment)
    file.close()
    terraform.init_terraform_profiles(username)
