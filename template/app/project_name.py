#!/usr/bin/env python3
# coding=utf-8

from hi_basic import *
import os
import argparse
import textwrap


def __info(args):
    curpath = os.path.dirname(os.path.abspath(__file__))
    appinfo = HiAppInfo(curpath)
    print(appinfo.name + " " + appinfo.version + " by " + appinfo.owner if appinfo.owner else "Unknown")
    # NOTE: Remember edit the "hikit-info.json" file, especially the "owner" and "remote"!
    pass


def __setup_parser():
    # Define the menu.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(HiText("menu_desc", """
        <PROJECT_NAME>
        This is the <PROJECT_NAME> project.
        Thank you for used.
        """)),
        epilog=textwrap.dedent("""
        """)
        )

    # Create sub commands.
    subparsers = parser.add_subparsers(
        title=HiText("menu_list_title", "Command List")
    )

    # Add command for show app info.
    parser_info = subparsers.add_parser(
        name="info",
        help=HiText("menu_info_help", "View tool's version and owner.")
        )

    parser_info.set_defaults(func=__info)

    # parse the input.
    args = parser.parse_args()

    if len(vars(args)) == 0:
        # if no input print help.
        parser.print_help()
    else:
        # select the function
        args.func(vars(args))
    pass


def main():
    """Entry."""
    __setup_parser()
    pass


if __name__ == "__main__":
    main()
    pass
