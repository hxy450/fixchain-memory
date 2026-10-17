# 子代理派发失败先按报错修正参数重试；确需改由主线程执行时，按 skill 降级条款补跑被派发的步骤

ID：`lesson-ae78da6f1a3669f6ef59` · 版本：2 · 阶段：plan/converge · 主题：[process/deferred-fulfillment](index.md)

概要：子代理派发失败先修参数重试，再按降级条款补跑

信号：`spawn_agent`, `api-inventory`

## 何时使用

执行编排阶段，spawn_agent 等子代理派发返回错误、准备改由编排会话自己完成时

## 适用情境

流水线 skill 要求派发子代理完成事实树、API 清单等步骤，并写有子代理不可用时的降级条款（如在汇合点前台串行跑一次）；派发因参数类型错误（如布尔参数传成字符串）失败，编排者准备把它当成环境限制。

## 原因

参数错误不等于环境不支持子代理；当作环境限制会让编排者压缩流程，跳过 skill 要求的产出步骤。来源中派发因上下文开关参数传成字符串而失败，生成者改由主线程自做全部工作，没有运行 API 清单提取，规格里没有网络契约，下游自拟基址与接口路径，页面也大量以空壳交付。

## 做法

1. 派发失败先读报错原文；属于参数类型或格式问题就修正后重试，不据此判定子代理不可用。
2. 确需改由主线程执行时，按 skill 的降级条款在前台补跑被派发的步骤（如 API 清单、事实树），拿到约定产物后再进入依赖它的规格或实现阶段；产物缺失时把对应小节标为阻塞。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [写页前读源 ViewModel/Service 列行为清单](../secondary-over-source/lesson-1997518f92b444368073.lesson.md)（共享 1 张卡）
- [服务地址沿键名追到源端常量，host 与环境不自拟](../../data/network-endpoint/lesson-246252824c631aa6eff5.lesson.md)（共享 1 张卡）
- [写文件以执行回执为准，覆盖入口页后内容断言读回](../claimed-without-receipt/lesson-776ed5eb216833c6b002.lesson.md)（共享 1 张卡）
- [规格所需值上游缺失时回源码补或标待核，不自拟](../unverified-as-fact/lesson-77ca67f164d77ec63cda.lesson.md)（共享 1 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6be1461999c00a7fe781](../../../../store/cases/case-6be1461999c00a7fe781/6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7.json) · 结论：diagnosis, rec-18c9be908c
  卡片版本：`6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7`
- [case-d45f9499eea676782c49](../../../../store/cases/case-d45f9499eea676782c49/8a8af69d09c260a2f91b4d42b1e6ef14d414e9e82845abfe7e45b1b7cd48f580.json) · 结论：diagnosis, rec-254ee4e9bb
  卡片版本：`8a8af69d09c260a2f91b4d42b1e6ef14d414e9e82845abfe7e45b1b7cd48f580`
