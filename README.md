# hikit

I often write some convenient Python tools, which I sometimes share with other team members for use. Over time, the version control and distribution deployment of these tools have become a complex issue. Moreover, others also write similar tools.

Since these tools are typically used internally within the team or personally, there are certain restrictions on open sourcing. Existing tools like pip or homebrew do not meet the needs for private tool distribution.

Therefore, I have developed this set of hikit tools for managing the distribution and deployment of private Python tools, and it also provides a series of commonly used base libraries. hikit is developed based on Git, including permission control, tool management, data storage, etc., all of which are completed through Git.

See also [中文说明](README-zh.md).

## How to Use

This section will tell you how to use this tool. Simply follow the steps below. If you wish to write your own tools, please skip to "How to Develop" and refer to "How to Submit."

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

If the installation fails, please check the error message. Currently, it only supports macOS and Linux, and works with bash and zsh. After successful installation, call the `hi` command to view the list of commands.

```shell
hi
```

Enter `hi [subcommand] -h` to view the help prompt for the subcommands.

### Configure hikit

The first time you open hikit to view the tool list,

```shell
hi list
```

It will request the input of the Git repository address where the tool list is stored. If you don't have one, you should first create a repository and ensure you have read and write permissions. Without write permissions, you can only access tool information but cannot publish or modify new tools. The address currently only supports Git and does not support https transmission.

Here is an example using the sample list:

```shell
hi list --setup git@github.com:DeepSkyStar/hikit-source.git
```

If you need to create your own software source, you can use the following command:

```shell
hi create --list my-source
```

Turn my-source (which can be defined by yourself) into a Git repository using `git init`, upload it to your specified Git server, and then use the `hi list --setup` command from the previous step to configure it.

hikit will default to the origin address at the time of installation as the source address for hikit itself, which can also be changed as needed. All hikit configuration information will be stored in `~/.hikit/config.json`, which can be directly viewed and modified.

If hikit is corrupted and cannot be opened, you can try to reinstall hikit following the installation steps.

### Install and Uninstall Tools

Enter:

```shell
hi list
```

To view the software available for installation from the current software source, and then choose to install. For example:

```shell
hi install hotkey
```

To uninstall a tool:

```shell
hi uninstall hotkey
```

During the development phase of a tool, you can bypass the release process and directly enter the tool's directory and call:

```shell
hi install
```

To install the local version of the tool, which will only create a soft link to the tool's executable file. To delete the soft link of the local version tool, you can use:

```shell
hi uninstall
```

Additionally, calling:

```shell
hi uninstall hi
```

Will uninstall hikit.

### Use Templates for Tool Development

You can quickly develop the tools you need using the provided templates:

```shell
hi create tool-name
```

You can also view `hi create -h` to create other types of tools, such as base libraries or templates for other languages.

### Version Management and Release

Modify the description and remote address in the `hikit-info.json` file and push it to a Git server. Tools with `hi dev` can perform some simple version management. Use `hi publish` to release the tool to the current source. Please confirm that you have direct write access to the main branch before publishing.

### hikit Directory Explanation

hikit only runs in the user directory. The `~/.hikit` is the running directory for hikit, where all installed software is stored.

`~/.hikit_user` stores all user data, including log information. Detailed directory definitions are in the `hi_path.py` file.

### How to Develop

To be done.

### How to Submit

To be done.
