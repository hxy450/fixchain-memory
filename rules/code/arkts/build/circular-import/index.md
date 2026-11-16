# 循环导入和顶层继承的初始化顺序

agent 会看到什么：产物里新加 import { X } from M 并 class … extends X（或在模块顶层、类静态初始化里用 X），而 M 直接或间接 import 回本文件，运行时报 ReferenceError: X is not initialized

## 规矩

- rule-cdac2bdb2f33｜新增 import 并让本文件类 extends 它前，先查对方是否间接导入回本文件，是则先移到叶子模块｜写错：新加 `import { X } from M` 并写 `class … extends X`（或在模块顶层、类静态初始化里用 X），而 M 直接或间接 import 回本文件；运行时报 `ReferenceError: X is not initialized`
