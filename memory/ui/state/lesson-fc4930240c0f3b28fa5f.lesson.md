# 定时器或帧回调里同步遍历 V2 可观察数组（@Trace、@Local，含嵌套行）做逐元素计算时，先用 UIUtils.getTarget 取原始数组

ID：`lesson-fc4930240c0f3b28fa5f` · 版本：1

[本主题](index.md)

## 何时使用

功能实现阶段，为 ArkUI V2 ViewModel 编写定时器或帧回调驱动、在 UI 线程同步运行的逐格或逐元素计算（模拟步进、批量统计）并读取可观察数组时

## 适用情境

源端在 delay 循环或协程里对普通 List 计算（同步耗时可忽略，周期约等于设定间隔）；目标把数据放在 @ObservedV2 模型的 @Trace 或组件 @Local 数组上，在 setTimeout 或帧回调里同步计算再整体提交。

## 原因

V2 对可观察数组（含嵌套数组的每一行）做观察代理，每次元素读取都走代理；网格类计算的读取次数是元素数乘邻域数，同步耗时直接加到每个周期上，短间隔档的实际速率明显低于源端。

## 做法

1. 回调开头用 UIUtils.getTarget(this.字段) 取原始数组，计算、比较、计数都用它；需要上一步数据的函数改为显式传入原始数组，不在函数里再读可观察字段。提交时仍整体赋值给可观察字段来触发刷新。

## 可选检查

- 源端周期是“等待 + 同步计算”时，打点实测单次回调的同步耗时，确认它相对最短间隔档可以忽略。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-31dcdb74eb848ff217c8](../../../store/cases/case-31dcdb74eb848ff217c8/360cfb87f8b2a47e9243a59d3a2beccef0b260bcbaed55d1f909b2a241f8fe46.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`360cfb87f8b2a47e9243a59d3a2beccef0b260bcbaed55d1f909b2a241f8fe46`
