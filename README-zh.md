# hikit
我经常都会写一些方便的python工具，有时候会分享给团队中的其他人使用，
久而久之，这些工具的版本管理和分发部署变成了一个很复杂的问题，而且其他人也会写一些类似的工具。

由于这些工具通常都是在团队内部或个人使用，对于开源有一定的限制，
现有类似pip或者homebrew之类的工具，难以实现私有工具分发的需求。

因此我写了这套hikit工具，用于管理私有python工具的分发和部署，并且提供了一系列常用的基础库。
hikit基于Git开发，包括权限控制，工具管理，数据存储等等都通过Git完成。

## 如何使用
这一章节将告诉你如何使用该工具，只需按以下步骤逐步进行即可。如果你希望编写自用的小工具请跳转到 [如何开发](#如何开发) 和查看 [如何提交](#如何提交).

### 安装hikit
把该仓库克隆到你喜欢的地方:

```shell
git clone git@github.com:DeepSkyStar/hikit.git
```

然后打开并安装:

```shell
cd hikit
./setup
```

安装失败请查看失败提示，目前仅支持**mac和linux，支持bash和zsh**。
安装成功后，调用hi命令查看命令列表。

```shell
hi
```

输入`hi [subcommand] -h`可以查看子命令的帮助提示。

### 配置hikit
在你第一次打开hikit查看工具列表时，

```shell
hi list
```

会请求输入存放工具列表的git仓库地址，如果你没有，你应该先创建一个仓库，并确保你拥有读写权限，如果没有写入权限，那么仅能获取工具信息，但无法发布或修改新工具。**地址目前暂时只支持git不支持https传输**。

以下以sample列表作为例子:
```shell
hi list --setup git@github.com:DeepSkyStar/hikit-source.git
```

如果需要创建自己的软件源，可以使用以下命令:
```shell
hi create --list my-source
```

将my-source(名字可以自行定义)用`git init`变成git仓库，上传到你指定的git服务器中，再使用上一步的`hi list --setup`命令进行配置即可。

hikit会默认以安装时的origin地址作为hikit自身的源地址，该地址也可根据需要进行更改。
所有的hikit的配置信息都会存放在`~/.hikit/config.json`, 可以直接查看和修改。

**如果hikit被破坏无法打开**，你可以尝试重新进行步骤[安装hikit](#安装hikit).

### 安装和卸载工具
输入

```shell
hi list
```

可以查看当前软件源可以安装的软件以及安装的情况，然后选择安装。如:

```shell
hi install hotkey
```

删除工具:

```shell
hi uninstall hotkey
```

在工具开发阶段，也可以绕开发布过程，直接进入该工具目录下，调用:

```shell
hi install
```

即可安装本地版本的工具，该过程仅会将工具的可执行文件做软链接。
删除本地版本工具的软链接，可以用:
```shell
hi uninstall
```

另，调用:

```shell
hi uninstall hi
```

可以卸载hikit。

### 使用模版进行工具开发
你可以通过提供的模版快速开发自己需要的工具:

```shell
hi create tool-name
```

也可以查看`hi create -h`，创建其他类型的工具，如基础库或其他语言的工具模版。

### 工具的版本管理和发布
修改工具`hikit-info.json`文件中的描述和远程地址，并传到一个git服务器上。
使用`hi dev`的工具可以进行一些简单的版本管理。
使用`hi publish`可以将工具发布到当前的源上。发布前请先确认有直接写入主分支的权限。

## hikit目录说明
hikit只会运行在用户目录下，其中`~/.hikit`为hikit的运行目录，安装的软件都会存放在这里。

`~/.hikit_user`存放所有的用户数据，包括日志信息。
详细目录定义在`hi_path.py`文件中。

## 如何开发
待补充。

## 如何提交
待补充。
