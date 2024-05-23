# hikit

I often write some convenient Python tools, and sometimes I share them with other team members. Over time, the version control and distribution deployment of these tools have become a complex issue. Moreover, other people also write similar tools.

Since these tools are usually used internally within the team or personally, there are certain restrictions on open source sharing. Existing tools like pip or homebrew do not meet the needs of private tool distribution.

Therefore, I have created this hikit tool to manage the distribution and deployment of private Python tools, and it also provides a series of commonly used basic libraries. Hikit is developed based on Git, including permission control, tool management, and data storage, all of which are completed through Git.

Also see [中文说明](README-zh.md)

[Release Note](release-notes.md)

## How to Use

This section will tell you how to use this tool. Simply follow the steps below. If you wish to write your own small tools, please skip to the section [How to develop](#how_to_dev).

### Install hikit

Clone this repository to your preferred location:

```shell
git clone git@github.com:DeepSkyStar/hikit.git
```

Then open and install:

```shell
cd hikit
./setup
```

If the installation fails, please check the error message. Currently, it only supports mac and linux, and bash and zsh. After successful installation, call the `hi` command to view the list of commands.

```shell
hi
```

Enter `hi [subcommand] -h` to view the help prompt for subcommands.

### Configure hikit

The first time you open hikit to view the tool list,

```shell
hi list
```

It will request the input of the Git repository address where the tool list is stored. If you don't have one, you should first create a repository and ensure you have read and write permissions. Without write permissions, you can only obtain tool information but cannot publish or modify new tools. The address currently only supports Git, not HTTPS transmission.

Here is an example using the sample list:

```shell
hi list --setup https://github.com/DeepSkyStar/hikit-source.git
```

If you need to create your own software source, you can use the following command:

```shell
hi create --list my-source
```

Turn my-source (which can be defined by yourself) into a Git repository using `git init`, upload it to your specified Git server, and then use the `hi list --setup` command from the previous step to configure it.

Hikit will default to the origin address at the time of installation as the source address for hikit itself, which can also be changed as needed. All hikit configuration information will be stored in the `~/.hikit/config.json` file, which can be directly viewed and modified.

If hikit is damaged and cannot be opened, you can try to reinstall hikit following the steps again.

### hipip
Hikit currently defaults to creating a virtual Python environment based on venv in the directory `~/.hikit/hienv`.
You can manage the packages of hienv using `hipip`.

### Install and Uninstall Tools

Enter:

```shell
hi list
```

To view the software available for installation from the current software source and their installation status, then choose to install. For example:

```shell
hi install hotkey
```

To delete a tool:

```shell
hi uninstall hotkey
```

During the tool development phase, you can bypass the release process and directly enter the tool directory and call:

```shell
hi install
```

This will install the local version of the tool, which will only create a soft link to the tool's executable file. To delete the soft link of the local version tool, use:

```shell
hi uninstall
```

Additionally, calling:

```shell
hi uninstall hi
```

Will uninstall hikit.

## <a id="how_to_dev">How to develop</a>

### Use Template for Tool Development

You can quickly develop the tools you need using the provided templates:

```shell
hi create tool-name
```

You can also view `hi create -h` to create other types of tools, such as basic libraries or templates for other languages.

### Tool Version Management and Release

Modify the description and remote address in the `hikit-info.json` file and push it to a Git server. Tools with `hi dev` can perform some simple version management. Use `hi publish` to release the tool to the current source. Please confirm that you have direct write access to the main branch before publishing.

### Hikit Directory Introduction

Hikit only runs in the user's directory. The `~/.hikit` is the running directory for hikit, and installed software will be stored here.

`~/.hikit_user` stores all user data, including log information. Detailed directory definitions are in the `hi_path.py` file.

### HiBasic Library Introduction

To be supplemented.

#### HiLog

Used for printing log information, user logs will be automatically saved in the `~/.hikit_user` directory. You can set the log output level with the `hi log` command.

#### HiConfig

A tool for quickly reading and writing user data based on JSON format.

For example:

```python
config = HiConfig("filepath")
config.writer["key"] = "value"
print(config["key"])
```

You can quickly read and write user data. Using `config.writer.autofill` or `config.w.a` will automatically fill in default values when the middle key does not exist, instead of reporting an error directly.

#### HiFile

Defines some common file operations, such as:

```python
stamp = HiFileStamp("file_path")

after some operations.

print(stamp.is_changed)
stamp.update()
```

You can check if the file has been updated during that period of time.

`HiFile.ensure_dirs()` can ensure that a certain path exists, and if not, it will automatically create the entire path. `HiFile.find_first()` will return the first found file.

## Maintenance Instructions

Hikit is quite unique; if it encounters any issues, it could lead to the invalidation of all local Hikit toolchains.
Therefore, if you wish to develop and maintain Hikit, it is essential to first understand its structure.
When making modifications to Hikit, proceed with special installations for different scenarios:

1. If you have modified the content of the hi_basic library: Use the command `python3 hi_basic_setup.py` to update the modified basic library.
2. If you have modified other parts of Hikit, use the command `python3 hi_setup.py` to install the modified tool.
3. Once the entire feature is fully developed, commit to the branch named feature/feature_name, and then use `hi install -b feature/feature_name` to conduct a complete integration test. After the test, submit a pull request (PR) to merge into the develop branch. Following approval and testing by the manager, it can be merged into the main branch.

## How to Contribute

### Branch and Commit Msg

This project follows the Git-Flow specification. If a commit only involves bug fixes and document updates, please mark it with [Fix]. If it includes feature updates, please mark it with [Feature].

### Coding Guidelines

This project follow some simple guidelines:

* All **class name** should start with an uppercase letter and use camel case, the prefix must be **Hi**, such as **HiConfig**.
* All **enumerations** and **constants** should be in uppercase, such as **USER_PATH**.
* All **internal variables** should be prefixed with an underscore '_'.
* All **variables, function names, file name, etc.**, without special provisions, should use lowercase letters with underscores, such as **hi_basic**.
