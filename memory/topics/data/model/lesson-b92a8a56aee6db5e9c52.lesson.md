# 把以字符串持久化的模型枚举映射到页面本地类型时，按模型枚举成员逐一 switch，不用成员名字符串变换去匹配

ID：`lesson-b92a8a56aee6db5e9c52` · 版本：4 · 阶段：execute · 主题：[data/model](index.md)

概要：持久化字符串枚举映射用逐成员 switch 不做名称变换

信号：`FRENCH_PRESS`, `toUpperCase`, `replace('_'`, `default:`, `Object.values`

## 何时使用

实现阶段把共享模型枚举（持久化为字符串）映射成页面本地枚举或资源时

## 适用情境

模型枚举的持久化值是带下划线的大写串（如 FRENCH_PRESS），页面本地枚举用驼峰成员名。

## 原因

驼峰名转大写后缺下划线，匹配失败的项落到默认分支，编译和结构审计都发现不了。来源中实现者一分钟前刚写好按成员 switch 的资源映射，接线列表页时仍用字符串变换比较，自查也只补了 toUpperCase。

## 做法

1. 按模型枚举成员逐一 switch，或复用已有的映射函数。
2. 遍历全部枚举成员跑一次映射，确认只有真正的默认项落到默认分支。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [验收条目实读源码段落，照抄比较符并给边界样例](../../process/enumeration-gaps/lesson-08854573a81a9fa03746.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [编排者代写切片前加载 worker 的全部派工输入](../../process/unloaded-input/lesson-b90d7f55409a3a34253d.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-37a2c6aacb67d1fc0aee](../../../../store/cases/case-37a2c6aacb67d1fc0aee/528d09b041c06639c78c05521087576cda7b79594f84cb4fcc278d8c2c62a75b.json) · 结论：diagnosis, rec-14fb510734
  卡片版本：`528d09b041c06639c78c05521087576cda7b79594f84cb4fcc278d8c2c62a75b`
