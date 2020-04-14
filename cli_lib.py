"""Repeated and useful functionality"""

import os
import argparse

def make_arg_parser(description: str) -> argparse.ArgumentParser:
    """Makes an argument parser with possible defaults from the environment"""
    unifi_host = os.getenv('UNIFI_HOST')
    unifi_port = os.getenv('UNIFI_PORT') or 8443
    unifi_user = os.getenv('UNIFI_USER')
    unif_pwd = os.getenv('UNIFI_PASSWD')
    unifi_site = os.getenv('UNIFI_SITE') or 'default'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--host", "-H",
                        dest="host",
                        default=unifi_host,
                        required=not unifi_host,
                        metavar="HOST_OR_IP",
                        help="Hostname or IP address of the controller")
    parser.add_argument("--port", "-p",
                        dest="port",
                        default=unifi_port,
                        required=False,
                        metavar="PORT",
                        help="Port number where the controller is hosting the API")
    parser.add_argument("--user", "-u",
                        dest="user",
                        default=unifi_user,
                        required=not unifi_user,
                        metavar="USERNAME",
                        help="Username with privileges to the API")
    parser.add_argument("--pass", "--pwd", "--password",
                        dest="password",
                        default=unif_pwd,
                        required=not unif_pwd,
                        metavar="PASSWORD",
                        help="Password for the user")
    parser.add_argument("--site", "-s",
                        dest="site",
                        default=unifi_site,
                        required=False,
                        metavar="SITE_NAME",
                        help=f"Site name on the controller, default is '{unifi_site}'")
    parser.add_argument("--json", "-j",
                        dest="json",
                        action="store_true",
                        default=False,
                        help="Show all records in JSON format")
    parser.add_argument("--list", "-l",
                        dest="list",
                        action="store_true",
                        default=False,
                        help="Show all records in human format")
    return parser
