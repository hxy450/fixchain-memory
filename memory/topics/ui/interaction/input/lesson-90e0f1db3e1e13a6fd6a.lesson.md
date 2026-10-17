# Android 平台公开正则常量按定义逐段移植并保持全串匹配语义

ID：`lesson-90e0f1db3e1e13a6fd6a` · 版本：2 · 阶段：execute/verify · 主题：[ui/interaction/input](index.md)

概要：平台正则按定义逐段移植并全串匹配

信号：`Patterns.WEB_URL`, `Patterns.EMAIL_ADDRESS`, `String.matches`, `(?i)`

## 何时使用

界面实现阶段，移植 Patterns.WEB_URL、Patterns.EMAIL_ADDRESS 等平台正则对用户输入的校验时

## 适用情境

源以 String.matches(Patterns.X.pattern()) 做全串校验，目标没有同名 API，需要自行提供正则。

## 原因

自拟的“实用等价式”会丢分支（如 IP 主机）或多收非法输入，而一般视觉验收不会输入这些边界值。

## 做法

1. 按公开定义逐段移植，目标正则引擎不支持的写法（内联 (?i)、UTF-16 代理对区间）改成等价写法，并保留全串匹配；仍有已知差异时登记具体会判错的输入。

## 可选检查

- 无法逐段移植、或确认与转交校验类不确定项前，用覆盖各分支的代表输入（带顶级域名的域名、IPv4 加端口、无 scheme、裸 localhost、IDN、前导空格）与源端预期离线对照

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [不补源端没有的元素；框架默认元素须保留](../../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-53fd6cc643582558ba6d](../../../../../store/cases/case-53fd6cc643582558ba6d/e085382b416f5dc8b20dcecc0bede224bb1df5873e210db40f105433387edcd8.json) · 结论：diagnosis, rec-e504086a24, rec-4782d62c8b, rec-1017a85f85
  卡片版本：`e085382b416f5dc8b20dcecc0bede224bb1df5873e210db40f105433387edcd8`
