# Hi Basic

提供一系列方便开发的基础Python模块，该模块会基于Python的标准安装方法安装到当前Python3的路径中。
由于这些模块会直接加载到用户的python3库中，因此在进行修改时请小心注意。

## 如何使用
`import eva_basic`

## 有哪些类
EVALog: 提供了标准化的EVA Log打印方法，方便打印日志。
EVAPath: 如果需要获取Eva以及你所开发的应用会安装到的位置，请使用里面的方法函数进行开发。
EVAConfig: 方便的持久化类，可以轻易地创建和保存一个持久化字典。
EVARepo: 用于对象化操作仓库的类。
EVADecorator: 提供一系列EVA特有的装饰器，比如@limitedby(),可以通过设定条件从而在运行时约束方法执行以免被错误调用。
