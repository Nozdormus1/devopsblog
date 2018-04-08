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

from botocore.client import ClientError


def install_terraform():
    local("wget -O /tmp/terraform.zip " + variables.terraform_url)
    local("sudo unzip -o /tmp/terraform.zip -d /opt/terraform")
    value = str("export PATH=$PATH:/opt/terraform")
    with open(os.environ['VIRTUAL_ENV'] + '/bin/postactivate', 'a+') as f:
        if not any(value == x.rstrip('\r\n') for x in f):
            f.write(value + '\n')


def init_bucket():
    session = boto3.Session(profile_name=variables.aws_profile)
    s3 = session.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=variables.states_bucket)
    except ClientError:
        bucket = s3.create_bucket(
            Bucket=variables.states_bucket,
            CreateBucketConfiguration={
                'LocationConstraint': variables.region
            })


@task
def init_terraform_profiles(username):
    init_bucket()
    environment=variables.environment()
    if not variables.profiles:
        print('No profiles were found, nothing to initialize')
    else:
        for profile in variables.profiles:
            init_terraform_backend(username, environment, profile)


def init_terraform_backend(username, environment, profile):
    keypath = '{}_{}/{}/terraform.tfstate'.format(username, environment, profile)

    with lcd(variables.cwd + '/terraform/profiles/{}'.format(profile)):
        local('/opt/terraform/terraform init ' \
            + '-backend-config \'region={}\' '.format(variables.region) \
            + '-backend-config \'bucket={}\' '.format(variables.states_bucket) \
            + '-backend-config \'key={}\' '.format(keypath) \
            + '-backend-config \'profile={}\''.format(variables.aws_profile))


def create_profile():
    #TODO
    print 'TODO'


@task
def update_terraform(username):
    install_terraform()
    init_terraform_profiles(username)


def apply_destroy_tf(username, environment, profile, action):
    sys.stdout.write('Please, confirm using your environment \'' + environment + '\' by typing it into prompt: ')
    choice = raw_input()
    if choice != environment:
        exit("\033[0;31m[ERROR] Invalid environment: '%s'\033[0m" % choice)
    tf_vars='{}'.format(helpers.terraform_configs_yaml_list(profile))
    print tf_vars
    tf_credentials=''
    if os.path.isfile(variables.cwd + '/terraform/configs/credentials.yaml'):
        tf_credentials='{}'.format(helpers.terraform_configs_yaml_list('credentials'))
    with lcd(variables.cwd + '/terraform/profiles/{}'.format(profile)):
        local('/opt/terraform/terraform {} '.format(action) \
            + '-var \'aws_profile={}\' '.format(variables.aws_profile) \
            + '-var \'username={}\' '.format(username) \
            + '-var \'environment={}\' '.format(environment) \
            + '-var \'region={}\' '.format(variables.region) \
            + tf_vars \
            + tf_credentials)


@task
def apply_tf(username, profile):
    apply_destroy_tf(username, variables.environment(), profile, 'apply')


@task
def destroy_tf(username, profile):
    apply_destroy_tf(username, variables.environment(), profile, 'destroy')
