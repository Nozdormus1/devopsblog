#!/usr/bin/env python2
#import textwrap

import os
import yaml
import boto3

from fabric.api import abort, task, puts, roles, local, env, lcd
from fabric import state
from fabric.task_utils import crawl


# For now instead of complexity inside code
# lets favour ssh config for handling ssh connections
#env.use_ssh_config = True
with open('global.yaml', 'r') as f:
    globals_yaml = yaml.load(f)
env.hosts = ["localhost"]
region = globals_yaml['region']
aws_profile = globals_yaml['aws_profile']
profiles = globals_yaml['profiles']
states_bucket = globals_yaml['states_bucket']
terraform_url = globals_yaml['terraform_url']
cwd = os.getcwd()


@task
def init(username, environment):
    install_terraform()
    configure_aws_credentials()
    init_bucket()
    for profile in profiles:
        init_terraform_backend(username, environment, profile)


@task
def install_terraform():
    local("wget -O /tmp/terraform.zip " + terraform_url)
    local("unzip -o /tmp/terraform.zip -d /opt/terraform")
    value = str("export PATH=$PATH:/opt/terraform")
    with open(os.environ['VIRTUAL_ENV'] + '/bin/postactivate', 'a+') as f:
        if not any(value == x.rstrip('\r\n') for x in f):
            f.write(value + '\n')


@task
def configure_aws_credentials():
    access_key = raw_input("Enter your aws access key: ")
    secret_key = raw_input("Enter your aws secret key: ")

    local("mkdir -p ~/.aws")
    credentials = '[{}]'.format(aws_profile) + '\naws_access_key_id = {}'.format(access_key) \
                  + '\naws_secret_access_key = {}'.format(secret_key)
    local('test -f ~/.aws/credentials && mv ~/.aws/credentials ~/.aws/credentials.bac || touch ~/.aws/credentials')
    local('echo \"' + credentials + '\" > ~/.aws/credentials')


@task
def init_bucket():
    session = boto3.Session(profile_name=aws_profile)
    s3 = session.resource('s3')
    if s3.Bucket(states_bucket) in s3.buckets.all() is False:
        bucket = s3.create_bucket(
            Bucket=states_bucket,
            CreateBucketConfiguration={
                'LocationConstraint': region
            })


@task
def init_terraform_backend(username, environment, profile):
    keypath = '{}_{}/{}/terraform.tfstate'.format(username, environment, profile)

    with lcd(cwd + '/terraform/{}'.format(profile)):
        local('/opt/terraform/terraform init ' \
            + '-backend-config \'region={}\' '.format(region) \
            + '-backend-config \'bucket={}\' '.format(states_bucket) \
            + '-backend-config \'key={}\' '.format(keypath) \
            + '-backend-config \'profile={}\''.format(aws_profile))


@task
def create_s3(username, environment):
    with lcd(cwd + '/terraform/init'):
        local('/opt/terraform/terraform apply ' \
            + '-var \'main_bucket_name={}-devopsblog-remote-states-tf\' '.format(username) \
            + '-var \'environment={}\' '.format(environment) \
            + '-var \'region={}\' '.format(region))


    #with open(os.path.expanduser('~/.aws/credentials', 'w'): pass
    #with open(os.path.expanduser('~/.aws/credentials'), 'a+') as f:
    #    f.write(credentials + '\n')
    #with open(os.path.expanduser('~/.aws/credentials'), 'a+') as f:
    #    block = ""
    #    i = 0
    #    for x in f:
    #        i += 1
    #        block = block + x.rstrip('\r\n') + '\n'
    #        if not x: continue
    #        if i%3 == 0:
    #            if not credentials == block:
    #                f.write(credentials + '\n')
    #            block = ""
    #            i = 0

#@task
#def help(name):
#    """
#    Show extended help for a task (e.g. 'fab help:search.reindex')
#
#    :param name   Name of fabric task to show help
#    """
#    task = crawl(name, state.commands)
#
#    if task is None:
#        abort("%r is not a valid task name" % task)
#
#    puts(textwrap.dedent(task.__doc__).strip())
