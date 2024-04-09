# hikits
这是一套用于管理私有python工具集的工具。

基于Git开发，包括权限控制，工具管理，数据存储等等都通过Git完成。

## 如何使用
这一章节将告诉你如何使用该工具，只需按以下步骤逐步进行即可。如果你希望对其进行修改，请跳转到 [如何开发](#如何开发) 和查看 [如何提交](#如何提交).

### 1. 安装
把该仓库克隆到你喜欢的地方

```shell
git clone https://github.com/HyperVisualArt/hikits.git
```

然后打开

```shell
cd hikits
./install
```
安装失败请查看失败提示。
在安装成功之后，在使用之前需要进行简单的配置。

### 2. 配置
在你第一次打开hikists查看工具列表时，

```shell
hikits list
```

会请求输入存放工具列表的git仓库地址，如果你没有，你应该先创建一个仓库，并确保你拥有读写权限，如果没有写入权限，那么仅能获取工具信息，但无法发布或修改新工具。**推荐使用ssh的方式**。

以sample列表为例，你可以在后续添加多个工具列表。
```shell
hikits list --add sample git@github.com:HyperVisualArt/hitkits-sample-list.git
```

hikits会默认以自身仓库的origin地址作为hitkits自身的源地址，该地址也可根据需要进行更改。
所有的hitkis的配置信息都会存放在`~/.hikits/config.json`, 你可以直接修改，**如果hikits被破坏无法打开**，你可以尝试重新进行步骤[1. 安装](#1.\ 安装).

### 3. 尝试
直接输入
```shell
hikits
```
或
```shell
hikits -h
```
可以查看各项功能的帮助说明，默认为英文，可以通过
```shell
hikits lang --switch "zh"
```
切换为中文或其他语言，可通过以下方式查看相关帮助说明
```shell
hikits lang --help
```

### 4. 使用模版开发工具
你可以通过提供的模版快速开发自己需要的工具，为了便于管理，这里提供了两种方法。
`hikits create name` 或者 hikits create -b name

### 5. 发布工具到工具列表中
提交app到hikits中，将app提交到hikits
hikits commit


## 如何开发

## 如何提交
