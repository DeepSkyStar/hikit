#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-12 20:37:40
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-22 21:55:37
FilePath: /hikit/hikit.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import sys
import argparse
import textwrap
from hi_basic import *
from hi_menu_display import *
from hi_installer import *


def __list(args):
    setup_list = args["setup"]
    if setup_list is not None:
        setup_list = setup_list[0]
    if setup_list is not None and setup_list:
        if HiPath.appsource() == setup_list:
            HiLog.info(HiText("menu_list_setup_source_same", "It's the same source!"))
        else:
            HiLog.info(HiText("menu_list_setup_start", "Try to setup list: ") + str(setup_list))
            HiSource.setup_source(setup_list)
            HiLog.info(HiText("menu_list_setup_source_successed", "Source change successed!"))
    else:
        if not HiPath.appsource():
            HiLog.info(HiText("menu_list_no_source_warning", "Source doesn't setup!"))
            HiLog.info(HiText("menu_list_no_source_warning_help", "Please use `hi list --setup <source-url>` setup source at first."))
        else:
            print("\n")
            print(HiMenuDisplay().pretty_list_display(source=HiSource()))
    pass


def __search(args):
    regex = args["regex"]
    find_apps = HiSource().search(regex)
    for app in find_apps:
        info = HiAppInfo.from_source(app)
        print(HiMenuDisplay.LIST_COLUMN_FORMAT.format(info.name) + " " + info.desc)
    pass


def __show(args):
    name = args["name"]
    if name:
        app = HiAppInfo.from_installed(name)
        if app is None:
            print(name + HiText("menu_show_not_exist", " not exist!"))
            return None
    else:
        # load from local
        app = HiAppInfo.from_local()
        if app is None:
            print(name + HiText("menu_show_not_exist", " not exist!"))
            return None

    print(HiText("menu_show_tile_name", "Name: ") + str(app.name))
    print(HiText("menu_show_tile_version", "Version: ") + str(app.version))
    print(HiText("menu_show_tile_owner", "Owner: ") + str(app.owner))
    print(HiText("menu_show_tile_contact", "Contact: ") + str(app.contact))
    print(HiText("menu_show_tile_remote", "Remote: ") + str(app.remote))
    print(HiText("menu_show_tile_desc", "Desc: ") + str(app.desc))
    print(HiText("menu_show_tile_command", "Commands: ") + str(app.commands))
    pass


def __update(args):
    only_list = args["all"]
    is_all = args["all"]
    name = args["name"]

    # Update hikit.
    if name and name == "hi" or is_all:
        HiLog.info(HiText("menu_update_app_start", "Start update: ") + "hikit")
        HiInstaller(HiAppInfo.from_installed("hi")).install()
        HiLog.info(HiText("menu_update_app_end", "Finished update: ") + "hikit")
        if not is_all:
            return None

    # Update Source list.
    if not HiPath.appsource():
        HiLog.info(HiText("menu_update_no_source_warning", "Source doesn't setup!"))
        HiLog.info(HiText("menu_update_no_source_warning_help", "Please use `hi list --setup <source-url>` setup source at first."))
        return None
    
    HiLog.info(HiText("menu_update_app_start", "Start update: ") + "source")
    HiSource().update()
    HiLog.info(HiText("menu_update_app_end", "Finished update: ") + "source")

    if is_all:
        # Update Apps.
        installed_apps = HiSource().installed_apps()
        for app in installed_apps:
            HiLog.info(HiText("menu_update_app_start", "Start update: ") + app)
            installer = HiInstaller(HiAppInfo.from_installed(app))
            installer.install()
            HiLog.info(HiText("menu_update_app_end", "Finished update: ") + app)
        return None
    
    if name:
        installed_apps = HiSource().installed_apps()
        if name in installed_apps:
            HiLog.info(HiText("menu_update_app_start", "Start update: ") + name)
            installer = HiInstaller(HiAppInfo.from_installed(name))
            installer.install()
            HiLog.info(HiText("menu_update_app_end", "Finished update: ") + name)
        else:
            HiLog.info(name + HiText("menu_update_app_not_installed", " is not installed!"))
        return None
    pass


def __install(args):
    is_all = args["all"]
    name = args["name"]
    branch = args["branch"]
    if branch is not None and len(branch) == 1:
        branch = branch[0]
        HiLog.info(HiText("menu_install_branch", "branch is ") + branch)
    else:
        branch = None
    # install all
    if is_all:
        for app in HiSource().group_list.all_apps():
            HiLog.info(app + HiText("menu_install_start", " start install..."))
            HiInstaller(HiAppInfo.from_source(app)).install(branch=branch)
            HiLog.info(app + HiText("menu_install_end", " finished install!"))
        return None
    # install app
    if name:
        app_info = HiAppInfo.from_source(name)
        if name == "hi":
            app_info = HiAppInfo.from_installed(name=name)
        if app_info is None:
            HiLog.info(name + HiText("menu_install_not_exist", " not exist!"))
            return None

        HiLog.info(name + HiText("menu_install_start", " start install..."))
        HiInstaller(app_info).install(branch=branch)
        HiLog.info(name + HiText("menu_install_end", " finished install!"))
        return None

    # install local
    app = HiAppInfo.from_local()
    if app is None:
        HiLog.info(HiText("menu_install_not_exist_local", "Current dir hasn't app!"))
        return None

    HiLog.info(os.getcwd() + HiText("menu_install_start", " start install..."))
    HiLocalInstaller(app).install()
    HiLog.info(os.getcwd() + HiText("menu_install_end", " finished install!"))
    pass


def __uninstall(args):
    # uninstall app
    name = args["name"]
    if name:
        if HiAppInfo.from_installed(name) is None:
            HiLog.info(name + HiText("menu_uninstall_not_exist", " not exist!"))
            return None
        HiLog.info(name + HiText("menu_uninstall_start", " start uninstall..."))
        HiInstaller(HiAppInfo.from_installed(name)).uninstall()
        HiLog.info(name + HiText("menu_uninstall_end", " finished uninstall!"))
        return None

    # uninstall local
    app = HiAppInfo.from_local()
    if app is None:
        HiLog.info(name + HiText("menu_uninstall_not_exist", " not exist!"))
        return None

    HiLog.info(os.getcwd() + HiText("menu_uninstall_start", " start uninstall..."))
    HiLocalInstaller(app).uninstall()
    HiLog.info(os.getcwd() + HiText("menu_uninstall_end", " finished uninstall!"))
    pass


def __create(args):
    name = args["name"]
    is_basic = args["basic"]
    is_list = args["list"]
    is_flutter = args["flutter"]
    is_force = args["force"]
    if is_list:
        HiSourceTemplate(name).generate_to_path(is_force=is_force)
    elif is_basic:
        HiPyModuleTemplate(name).generate_to_path(is_force=is_force)
    elif is_flutter:
        HiFlutterTemplate(name).generate_to_path(is_force=is_force)
    else:
        HiAppTemplate(name).generate_to_path(is_force=is_force)
    path = os.path.join(os.getcwd(), name)
    HiLog.info(HiText("menu_create_finished", "Template already generate to ") + path)
    pass


def __publish(args):
    group = args["group"]

    app_info = HiAppInfo.from_local()
    if app_info is None:
        HiLog.warning(HiText("menu_publish_error", "Current dir not a app!"))
        return None

    if HiSource().add_app(app=app_info, group=group):
        HiLog.info(HiText("menu_publish_successed", "App already publish to local source, waiting for upload..."))
        HiSource().publish()
        HiLog.info(HiText("menu_publish_successed_upload", "Source upload successed!"))
    else:
        HiLog.warning(HiText("menu_publish_failed", "Group not exist!"))
    pass


def __alias(args):
    command = args["command"]
    alias = args["alias"]
    HiInstaller.make_alias(command, alias)
    HiLog.info(alias + HiText("menu_alias_finished", " already added!"))
    pass


def __reset_alias(args):
    HiInstaller.clean_alias()
    HiLog.info(HiText("menu_reset_alias_finished", "Alias already clean up!"))
    pass


def __lang(args):
    generate = args["generate"]
    set_lang = args["set"]
    
    if generate:
        appinfo = HiAppInfo.from_local()
        if appinfo is None:
            HiLog.warning(HiText("menu_lang_generate_lang_not_app", "It's not a hi tool!"))
            return None
        
        HiMultiLang.generate_lang_file(os.getcwd())
        print(HiText("menu_lang_generate_lang_to", "Generate: ") + HiMultiLang.find_lang_file(os.getcwd()))
        return None

    if set_lang and len(set_lang) > 0:
        HiConfig().writer[HiMultiLang.LANG_KEY] = set_lang[0]
        print(HiText("menu_lang_set_lang_to", "Language change to: ") + set_lang[0])
        return None

    current_lang = HiConfig()[HiMultiLang.LANG_KEY]
    if not current_lang:
        current_lang = "en"
    print(HiText("menu_lang_current_lang", "Current Lang is:") + current_lang + "\n")
    pass


def __dev(args):
    HiLog.warning("Not support Yet!")
    pass


def __log(args):
    is_critical = args["critical"]
    is_error = args["error"]
    is_warning = args["warning"]
    is_info = args["info"]
    is_debug = args["debug"]
    is_notset = args["notset"]
    if is_critical:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.CRITICAL
    elif is_error:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.ERROR
    elif is_warning:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.WARNING
    elif is_info:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.INFO
    elif is_debug:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.DEBUG
    elif is_notset:
        HiConfig.hikit_config().writer[HIKIT_LOG_LEVEL] = HiLogLevel.NOTSET
    else:
        HiLog.info(HiText("menu_log_level_not_change", "Log level:") + str(HiConfig.hikit_config()[HIKIT_LOG_LEVEL]))
        return None
    HiLog.info(HiText("menu_log_level_change_text", "Log level change to: ") + str(HiConfig.hikit_config()[HIKIT_LOG_LEVEL]))
    pass


def __setup_parser():
    # The major intro
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(HiText("menu_desc", "Hikit\nYou can use `hi -h` to get more help.")),
        epilog=textwrap.dedent(HiText("menu_epilog", "Have a good life ~"))
        )

    # Create sub commands.
    subparsers = parser.add_subparsers(
        title=HiText("menu_title", "Command List"),
    )

    # List apps.
    parser_list = subparsers.add_parser(
        name="list",
        help=HiText("menu_list_help", "List all tools"),
        description=textwrap.dedent(HiText("menu_list_desc", """
        Use `hi list` can list all tools.
        Use `hi list --setup [list remote address]` can change list.
        Use `hi update` or `hi update --list` can update list.
        """))
        )

    parser_list.add_argument(
        '-s',
        '--setup',
        help=HiText("menu_list_setup_desc", "Setup a new list source. Only Support git."),
        nargs=1,
        action="store",
        )

    parser_list.set_defaults(func=__list)

    # Search apps.
    parser_search = subparsers.add_parser(
        name="search",
        help=HiText("menu_search_help", "Use regular expressions to search app in list."),
        description=textwrap.dedent(HiText("menu_search_desc", """
        Use `hi search [regex string]` can use regular expressions to search app in list.
        """))
        )

    parser_search.add_argument(
        'regex',
        help=HiText("menu_search_regex_desc", "The regex use to search apps.")
        )

    parser_search.set_defaults(func=__search)

    # Show app's infomation.
    parser_show = subparsers.add_parser(
        name="show",
        help=HiText("menu_show_help", "Show tools infomation."),
        description=textwrap.dedent(HiText("menu_show_desc", """
        Use `hi show [app name]` can show the app's infomation.
        """))
        )

    # parser_show.add_argument(
    #     "--release-note",
    #     help=HiText("menu_show_release_note_desc", "Show app's release note."),
    #     action="store_true"
    # )

    parser_show.add_argument(
        "name",
        help=HiText("menu_show_name_desc", "App's name."),
        nargs="?",
        default=""
    )

    parser_show.set_defaults(func=__show)

    # Update apps, including hikit itself.
    parser_update = subparsers.add_parser(
        name="update",
        help=HiText("menu_update_help", "Update apps and list."),
        description=textwrap.dedent(HiText("menu_update_desc", """
        use,
        hi update
        will update list automatically, install all default tools,
        and update all installed tools.

        use,
        hi update hi
        to update hikit.
                                           
        use,
        hi update [app name]
        to update app.

        use,
        hi update --all or hi update -a,
        Will update list, hikit and installed apps.
        """))
        )

    parser_update.add_argument(
        '-a',
        '--all',
        help=HiText("menu_update_list_desc", "Update all."),
        action="store_true"
        )

    parser_update.add_argument(
        'name',
        help=HiText("menu_uninstall_name_desc", "The app's name or a local app' path. Not necessary."),
        nargs='?',
        default=""
        )

    parser_update.set_defaults(func=__update)

    # Install app, including hikit itself.
    parser_install = subparsers.add_parser(
        name="install",
        help=HiText("menu_install_help", "Install app."),
        description=textwrap.dedent(HiText("menu_install_desc", """
        Use `hi install [app name]`, can install the app.
        If use `hi install` directly inside the local app dir,
        can install app from local.
        """))
        )

    parser_install.add_argument(
        'name',
        help=HiText("menu_install_name_desc", "The app's name or a local app' path. Not necessary."),
        nargs='?',
        default=""
        )

    parser_install.add_argument(
        '-a',
        '--all',
        help=HiText("menu_install_all_desc", "Install all apps."),
        action="store_true"
        )
    
    parser_install.add_argument(
        '-b',
        '--branch',
        help=HiText("menu_install_branch_desc", "Install app by another branch."),
        nargs=1,
        action="store"
        )

    parser_install.set_defaults(func=__install)

    # Uninstall apps including hikit itself.
    parser_uninstall = subparsers.add_parser(
        name="uninstall",
        help=HiText("menu_uninstall_help", "Uninstall app."),
        description=textwrap.dedent(HiText("menu_uninstall_desc", """
        Use `hi uninstall [app name]`, can uninstall the app.
        also can run in a local app' dir, the same as `install`.
        Use `hi uninstall hikit`, can uninstall the hikit.
        """))
        )

    parser_uninstall.add_argument(
        'name',
        help=HiText("menu_uninstall_name_desc", "The app's name or a local app' path. Not necessary."),
        nargs='?',
        default=""
        )

    parser_uninstall.set_defaults(func=__uninstall)

    # Creat apps.
    parser_create = subparsers.add_parser(
        name="create",
        help=HiText("menu_create_help", "Provide template for create app and list."),
        description=textwrap.dedent(HiText("menu_create_desc", """
        Use `hi create [name]` will create a normal app template in
        current dir.
        Use `hi create --basic [name]` will create a python module
        template in current dir.
        Use `hi create --list [name]` will create a app list template
        in current dir.
        """))
        )

    parser_create.add_argument(
        'name',
        help=HiText("menu_create_name_desc", "The tool's name.")
        )

    parser_create.add_argument(
        '-b',
        '--basic',
        help=HiText("menu_create_basic_desc", "The python module template."),
        action="store_true"
        )

    parser_create.add_argument(
        '-l',
        '--list',
        help=HiText("menu_create_list_desc", "The app list template."),
        action="store_true"
        )

    parser_create.add_argument(
        '--flutter',
        help=HiText("menu_create_flutter_desc", "The flutter app template."),
        action="store_true"
        )

    parser_create.add_argument(
        '--force',
        help=HiText("menu_create_force_desc", "Is it force create."),
        action="store_true"
        )

    parser_create.set_defaults(func=__create)

    # Publish app.
    parser_publish = subparsers.add_parser(
        name="publish",
        help=HiText("menu_publish_help", "Publish app to list, will create a branch and push. (Need merge by hand.)"),
        description=textwrap.dedent(HiText("menu_publish_desc", """
        In the developing app's dir, use `hi publish`,
        will publish this tool to hikit's app list,
        and then create a new branch push to the list source,
        need merge it to master by hand.

        NOTE, if app's infomation change also need to publish again.
        """))
        )

    parser_publish.add_argument(
        "group",
        help=HiText("menu_publish_group_desc", "Publish app to a exist group"),
    )
    # TODO: Add argument to change url.
    parser_publish.set_defaults(func=__publish)

    # For make alias.
    parser_alias = subparsers.add_parser(
        name="alias",
        help=HiText("menu_alias_help", "For make some alias."),
        description=textwrap.dedent(HiText("menu_alias_desc", """
        Use `hi alias [command] [alias]` can make alias for command.
        """))
        )

    parser_alias.add_argument(
        'command',
        help=HiText("menu_alias_command_desc", "The command.")
        )

    parser_alias.add_argument(
        'alias',
        help=HiText("menu_alias_alias_desc", "The alias.")
        )

    parser_alias.set_defaults(func=__alias)

    # For clean all alias.
    parser_reset_alias = subparsers.add_parser(
        name="reset-alias",
        help=HiText("menu_reset_alias_help", "Clean all alias."),
        description=textwrap.dedent(HiText("menu_reset_alias_desc", """
        Use `hi reset-alias` will clean all defined alias.
        """))
        )

    parser_reset_alias.set_defaults(func=__reset_alias)

    parser_lang = subparsers.add_parser(
        name="lang",
        help=HiText("menu_lang_help", "For enable multi lang."),
        description=textwrap.dedent(HiText("menu_alias_desc", """
        Use `hi alias [command] [alias]` can make alias for command.
        """))
        )
    
    parser_lang_group = parser_lang.add_mutually_exclusive_group()
    parser_lang_group.add_argument(
        "-s",
        "--set",
        help=HiText("menu_lang_set_desc", "Change language, default is en. cn is Chinese"),
        nargs=1,
        action="store"
    )    
    parser_lang_group.add_argument(
        "-g",
        "--generate",
        help=HiText("menu_lang_generate_desc", "Generate multi lang file for the project."),
        action="store_true"
    )
    # parser_lang_group.add_argument(
    #     "-c",
    #     "--current",
    #     help=HiText("menu_lang_current_desc", "Get current language."),
    #     action="store_true"
    # )

    parser_lang.set_defaults(func=__lang)

    # Some dev tools.
    parser_dev = subparsers.add_parser(
        name="dev",
        help=HiText("menu_dev_help", "Some dev tools."),
        description=textwrap.dedent(HiText("menu_dev_desc", """
        For clean cache,
        Use `hi dev --pyclean` will clean all python cache.

        For Release note,
        Use `hi dev --major [desc]` will update the first version number.
        Use `hi dev --feature [desc]` will update the second version number.
        Use `hi dev --bugfix [desc]` will update the third version number.
        """))
    )

    parser_dev.add_argument(
        "-p",
        "--pyclean",
        help=HiText("menu_dev_pyclean_desc", "Clean all python cache."),
        action="store_true"
    )

    parser_dev.add_argument(
        "-m",
        "--major",
        help=HiText("menu_dev_major_desc", "Update the first version number."),
        nargs=1,
        action="store"
    )

    parser_dev.add_argument(
        "-f",
        "--feature",
        help=HiText("menu_dev_feature_desc", "Update the second version number."),
        nargs=1,
        action="store"
    )

    parser_dev.add_argument(
        "-b",
        "--bugfix",
        help=HiText("menu_dev_bugfix_desc", "Update the third version number."),
        nargs=1,
        action="store"
    )

    parser_dev.set_defaults(func=__dev)

    # Log control
    parser_log = subparsers.add_parser(
        name="log",
        help=HiText("menu_log_help", "Log level control."),
        description=textwrap.dedent(HiText("menu_log_desc", """
        For log level control.
        Use `hi log --debug` will change to debug level.
        Other same as above
        """))
    )

    parser_log_group = parser_log.add_mutually_exclusive_group()

    parser_log_group.add_argument(
        "-c",
        "--critical",
        help=HiText("menu_log_critical_desc", "only show Critical log."),
        action="store_true"
    )

    parser_log_group.add_argument(
        "-e",
        "--error",
        help=HiText("menu_log_error_desc", "only show Error/Critical log."),
        action="store_true"
    )

    parser_log_group.add_argument(
        "-w",
        "--warning",
        help=HiText("menu_log_warning_desc", "only show Error/Critical/Warning log."),
        action="store_true"
    )

    parser_log_group.add_argument(
        "-i",
        "--info",
        help=HiText("menu_log_info_desc", "only show Error/Critical/Warning/Info log."),
        action="store_true"
    )

    parser_log_group.add_argument(
        "-d",
        "--debug",
        help=HiText("menu_log_debug_desc", "only show Error/Critical/Warning/Info/Debug log."),
        action="store_true"
    )

    parser_log_group.add_argument(
        "-n",
        "--notset",
        help=HiText("menu_log_notset_desc", "Show all log."),
        action="store_true"
    )

    parser_log.set_defaults(func=__log)

    # Parse args.
    args = parser.parse_args()

    if len(vars(args)) == 0:
        # If no args print help.
        parser.print_help()
    else:
        # If have args enter the function.
        args.func(vars(args))
    pass


def main():
    """Entry point."""
    __setup_parser()
    pass


if __name__ == "__main__":
    main()
    pass
