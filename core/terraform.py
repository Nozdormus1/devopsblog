#!/usr/bin/env python2

import variables

import os
import yaml
import boto3

from fabric.api import abort, task, puts, roles, local, env, lcd
from fabric import state
from fabric.task_utils import crawl


@task
def install_terraform():
    local("wget -O /tmp/terraform.zip " + variables.terraform_url)
    local("sudo unzip -o /tmp/terraform.zip -d /opt/terraform")
    value = str("export PATH=$PATH:/opt/terraform")
    with open(os.environ['VIRTUAL_ENV'] + '/bin/postactivate', 'a+') as f:
        if not any(value == x.rstrip('\r\n') for x in f):
            f.write(value + '\n')


@task
def init_bucket():
    session = boto3.Session(profile_name=variables.aws_profile)
    s3 = session.resource('s3')
    if s3.Bucket(variables.states_bucket) in s3.buckets.all() is False:
        bucket = s3.create_bucket(
            Bucket=variables.states_bucket,
            CreateBucketConfiguration={
                'LocationConstraint': variables.region
            })


@task
def init_terraform_profiles(username, environment):
    if not variables.profiles:
        print('No profiles were found, nothing to initialize')
    else:
        for profile in variables.profiles:
            init_terraform_backend(username, environment, profile)


@task
def init_terraform_backend(username, environment, profile):
    keypath = '{}_{}/{}/terraform.tfstate'.format(username, environment, profile)

    with lcd(variables.cwd + '/terraform/{}'.format(profile)):
        local('/opt/terraform/terraform init ' \
            + '-backend-config \'region={}\' '.format(variables.region) \
            + '-backend-config \'bucket={}\' '.format(variables.states_bucket) \
            + '-backend-config \'key={}\' '.format(keypath) \
            + '-backend-config \'profile={}\''.format(variables.aws_profile))


@task
def create_profile():
    #TODO
    print 'TODO'


@task
def apply_tf(username, environment, profile):
    #TODO
    tf_vars=""
    for key, value in yaml.load(open(variables.cwd + '/terraform/{}.yaml'.format(profile)))['global'].iteritems():
        tf_vars+='-var \'{}={}\' '.format(key, value)
    print tf_vars
    with lcd(variables.cwd + '/terraform/{}'.format(profile)):
        local('/opt/terraform/terraform apply ' \
            + '-var \'username={}\' '.format(username) \
            + '-var \'environment={}\' '.format(environment) \
            + '-var \'region={}\' '.format(variables.region) \
            + tf_vars)
