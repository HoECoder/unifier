#!/usr/bin/env python3
"""Script to get 5 minute reports out of the local controller"""

import os
import sys

try:
    from dotenv import load_dotenv
    HAVE_DOT_ENV = True
except ImportError:
    HAVE_DOT_ENV = False

from unifierlib import Controller
from unifierlib.utility import summarize_stats as summarize_minutes

import click

if HAVE_DOT_ENV:
    load_dotenv()

DATETIME_FORMAT = os.getenv('UNIFI_DT_FMT') or '%y-%m-%d %H:%M:%S'

def summarize_stats(controller: Controller,
                    do_json=False,
                    do_list=False):
    """Collects and summarizes statistics"""
    if not controller.logged_in:
        return

    stats = controller.get_minutely_stats()
    summarize_minutes(stats,
                      DATETIME_FORMAT,
                      do_json=do_json,
                      do_list=do_list)

@click.command()
@click.option("--host", "-H", "host",
              prompt=True,
              envvar="UNIFI_HOST",
              help="Hostname or IP address of the controller")
@click.option("--port", "-p", "port",
              envvar='UNIFI_PORT',
              default=8443,
              show_default=True,
              help="Port number where the controller is hosting the API")
@click.option("--user", "-u", "user",
              envvar='UNIFI_USER',
              prompt=True,
              help="Username with privileges to the API")
@click.option("--password", "--pass", "--pwd", "-P", "password",
              envvar='UNIFI_PASSWD',
              prompt=True,
              required=True,
              help="Password for the user")
@click.option("--site", "-s", "site",
              envvar='UNIFI_SITE',
              default="default",
              show_default=True,
              help="Site name on the controller")
@click.option("--json", "-j", "do_json",
              default=False, is_flag=True,
              help="Show all records in JSON format")
@click.option("--list", "-l", "do_list",
              default=False, is_flag=True,
              help="Show all records in human format")
def main(host, port, user, password, site, do_json, do_list):
    """Gather minutely data usage stats from a Unfi Controller."""

    controller = Controller(host,
                            port,
                            user,
                            password,
                            site=site,
                            ssl_verify=False)
    if not controller.logged_in:
        return

    summarize_stats(controller,
                    do_json=do_json,
                    do_list=do_list)

if __name__ == "__main__":
    #pylint: disable=no-value-for-parameter
    main()
