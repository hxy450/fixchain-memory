# 翻译条件表达式与分支时保留源的分组与分支范围：布尔异或在 ArkTS 写成 !==，列真值表，源码没有 else 就不新增分支

ID：`lesson-381ebc5899e92cbd23a2` · 版本：3

[本主题](index.md)

## 何时使用

实现阶段，翻译含异或、与或组合的三元或条件表达式（如气泡箭头位置、方向相关分支），或移植带守卫的 if 分支（空输入守卫、缺参数不动作）时

## 适用情境

源表达式形如 a + ((x ^ y) ? 0 : b)，转述时容易丢掉内层括号或取反分支；或源端计算入口只有 if (a != null && b != null) 分支、没有 else，目标准备在输入无效时新增清空结果或复位界面的分支。

## 原因

口头转述会改变运算优先级或真假分支，结果在常见配置下恰好取反；ArkTS 编译器不接受 boolean 操作数的 ^，照抄会编译失败。源码没有 else 时，新增的清空分支会把“不动作”变成“清空界面”。

## 做法

1. 保留源码的括号分组，对每个布尔输入列真值表（例如 LTR 下 y 为真、假各取哪个分支），在注释写明各情况的结果后再写代码；Java 的布尔异或 x ^ y 在 ArkTS 写成 x !== y（DevEco SDK 的 ets-loader 内置 ohos-typescript 对 boolean 操作数的 ^ 报诊断 2447，并建议改用 !==）。
2. 移植守卫分支时按源码 if 的范围翻译：源码没有 else 就不新增清空或复位界面的分支；服务层返回的空结果不被页面无条件拿去覆盖界面，页面在调用前判断并直接返回。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-1907ba587e6b1439f17d](../../../store/cases/case-1907ba587e6b1439f17d/3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a`
- [case-74bcab538b062ee7cac8](../../../store/cases/case-74bcab538b062ee7cac8/b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f.json) · 结论：recommendation:3
  卡片版本：`b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f`
