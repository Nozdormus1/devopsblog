#!/usr/bin/env python2
#import textwrap

import os
import yaml
import boto3

import core

from fabric.api import abort, task, puts, roles, local, env, lcd
from fabric import state
from fabric.task_utils import crawl


# For now instead of complexity inside code
# lets favour ssh config for handling ssh connections
#env.use_ssh_config = True


@task
def init(username, environment):
    core.install_terraform()
    core.install_packer()
    core.configure_aws_credentials()
    core.change_env(username, environment)


#@task
#def help(name):
#TODO
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
