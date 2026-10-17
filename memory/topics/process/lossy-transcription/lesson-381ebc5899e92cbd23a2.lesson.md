# 翻译含布尔组合的条件表达式时保留括号并列真值表

ID：`lesson-381ebc5899e92cbd23a2` · 版本：2 · 阶段：execute · 主题：[process/lossy-transcription](index.md)

概要：布尔组合条件逐字保留括号并列真值表

信号：`LTR`

## 何时使用

实现阶段，翻译含异或、与或组合的三元或条件表达式（如气泡箭头位置、方向相关分支）时

## 适用情境

源表达式形如 a + ((x ^ y) ? 0 : b)，转述时容易丢掉内层括号或取反分支。

## 原因

口头转述会改变运算优先级或真假分支，结果在常见配置下恰好取反。

## 做法

1. 逐字保留括号，对每个布尔输入列真值表（例如 LTR 下 y 为真、假各取哪个分支），在注释写明各情况的结果后再写代码。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [气泡整体着色用 popupColor，不只给内容加背景](../../ui/dialog/frame/lesson-05dc4eb9548bf3fef6ae.lesson.md)（共享 1 张卡）
- [占位只登记输入缺值的情况，能实现的当场实现](../deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1907ba587e6b1439f17d](../../../../store/cases/case-1907ba587e6b1439f17d/3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a.json) · 结论：diagnosis, rec-cc8ff83d54
  卡片版本：`3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a`
