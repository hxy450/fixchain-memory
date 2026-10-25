# 带系统确认框的媒体接口（如 deleteAssets）被拒时单列用户取消：按设备实测判别，不把 201 一律报成权限不足

ID：`lesson-c2f15aa3af3945ddfa8e` · 版本：1

[本主题](index.md)

## 何时使用

实现或返修带系统确认框的媒体删除、写入接口的失败提示与测试替身时

## 适用情境

目标接口先校验权限再弹系统确认框，Promise 拒绝既可能是权限不足，也可能是用户点了取消；d.ts 只把 201 记为 Permission denied，未记载取消码。源端失败只记日志、不提示；已有测试可能把“拒绝或取消”定为不提示。

## 原因

把一个错误码当成单一含义时，用户取消会显示“无权删除”一类误导提示；用假定的取消码写测试替身，测试与真机分叉，误报长期存活。已观察：API 24 设备上在确认框点取消，deleteAssets 的 Promise 以 code 201、message 'user deny' 异步拒绝，与真正的权限不足同码；该 message 是否为稳定契约未见文档。

## 做法

1. 写提示映射前在设备上点一次取消，记录拒绝路径（同步抛出还是 Promise 拒绝）与 code/message；取消作为独立结果照源端处理（只记日志、不提示、不清除媒体记录），只有真正失败才提示失败或权限不足。
2. 测试替身使用设备实测的取消值，分别覆盖同步异常、权限申请失败与确认框取消；改写已有“拒绝或取消”用例的期望前，先拆成取消与失败两个用例。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-cd4f1c37e7e321bb50d6](../../../store/cases/case-cd4f1c37e7e321bb50d6/4fb0ffcdece4d841ec76fdecf759848b61eb9cfea967109883a5f5f07c53f8f2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`4fb0ffcdece4d841ec76fdecf759848b61eb9cfea967109883a5f5f07c53f8f2`
