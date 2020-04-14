#!/usr/bin/env python3
"""Script to get hourly reports out of the local controller"""

import os
import sys

try:
    from dotenv import load_dotenv
    HAVE_DOT_ENV = True
except ImportError:
    HAVE_DOT_ENV = False

from unifierlib import Controller
from unifierlib.utility import summarize_stats as summarize_hourlies

from cli_lib import make_arg_parser

PROGRAM_DESC = "Collect Hourly Stats From the Controller"

if HAVE_DOT_ENV:
    load_dotenv()

DATETIME_FORMAT = os.getenv('UNIFI_DT_FMT') or '%y-%m-%d %H:%M:%S'

def summarize_stats(controller: Controller,
                    do_json=False,
                    do_list=False):
    """Collects and summarizes statistics"""
    if not controller.logged_in:
        return

    stats = controller.get_hourly_stats()
    summarize_hourlies(stats,
                       DATETIME_FORMAT,
                       do_json=do_json,
                       do_list=do_list)

def main():
    """Main Entry Point"""
    parser = make_arg_parser(PROGRAM_DESC)
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

    summarize_stats(controller,
                    do_json=args.json,
                    do_list=args.list)

if __name__ == "__main__":
    main()
