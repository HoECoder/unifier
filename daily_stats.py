#!/usr/bin/env python3
"""Script to get daily reports out of the local controller"""

import os
import sys
import argparse

try:
    from dotenv import load_dotenv
    HAVE_DOT_ENV = True
except ImportError:
    HAVE_DOT_ENV = False

from unifierlib import Controller

PROGRAM_DESC = "Collect Daily Stats From the Controller"

if HAVE_DOT_ENV:
    load_dotenv()

WAN_TX_KEY = "wan-tx_bytes"
WAN_RX_KEY = "wan-rx_bytes"
TIME_KEY = "time"
NUM_DIGITS = 2

def _make_arg_parser():
    """Makes an argument parser with possible defaults from the environment"""
    unifi_host = os.getenv('UNIFI_HOST')
    unifi_port = os.getenv('UNIFI_PORT') or 8443
    unifi_user = os.getenv('UNIFI_USER')
    unif_pwd = os.getenv('UNIFI_PASSWD')
    unifi_site = os.getenv('UNIFI_SITE') or 'default'
    parser = argparse.ArgumentParser(description=PROGRAM_DESC)
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
    return parser

def summarize_stats(controller: Controller):
    """Collects and summarizes statistics"""
    if not controller.logged_in:
        return

    stats = controller.get_daily_stats()
    if not stats:
        return
    total_tx = 0
    total_rx = 0
    for stat_entry in stats:
        total_tx += stat_entry[WAN_TX_KEY]
        total_rx += stat_entry[WAN_RX_KEY]
    total = total_rx + total_tx

    total_tx = round(total_tx / 1024**3, NUM_DIGITS)
    total_rx = round(total_rx / 1024**3, NUM_DIGITS)
    total = round(total / 1024**3, NUM_DIGITS)

    print(f'Total: Up: {total_tx} GB; Down: {total_rx} GB; Total: {total} GB')

def main():
    """Main Entry Point"""
    parser = _make_arg_parser()
    args = parser.parse_args()

    if not args.password:
        print("No password set!")
        parser.print_help()
        sys.exit(1)

    controller = Controller(args.host,
                            args.port,
                            args.user,
                            args.password,
                            site=args.site,
                            ssl_verify=False)
    if not controller.logged_in:
        return

    summarize_stats(controller)

if __name__ == "__main__":
    main()
