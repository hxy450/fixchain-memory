# 源端 getter 读打开期缓存或逐帧回调写入的相机元数据时，目标改为提交后快照或事件订阅缓存，不在 getter 里调同步相机服务接口

ID：`lesson-2fd3f5f24a7571d3eded` · 版本：1

[本主题](index.md)

## 何时使用

相机控制器实现阶段，为源端能力枚举 getter 与 capture result 字段（ISO、曝光时间）确定目标取值通道，或在 UI 访问器、定时绘制中消费控制器值时

## 适用情境

源端打开时缓存 CameraCharacteristics 派生的能力，或由 onCaptureCompleted 写入 capture_result_* 字段，调用方在 UI 访问、定时绘制或会话切换中高频读取；目标对应接口（getSupportedOutputCapability、session.isFocusModeSupported/getSupportedIsoRange、getIso/getExposureDuration）是同步相机服务调用，另有 ISO/曝光信息变化事件可订阅。

## 原因

把读内存字段直译成每次调用同步相机服务接口，调用成本从零变成跨进程往返，结果还随调用时刻的会话状态变化；被定时绘制调用时会卡住主线程。只按 getter 名在 SDK 中检索，找到的是同步查询，而源端数据来自回调。

## 做法

1. 先打开源端字段的赋值点（打开时读一次，还是 onCaptureCompleted 等回调逐帧写入），再在目标 SDK 找同一来源：能力在初次会话 commitConfig 后读一次快照，显示尺寸、zoom 等派生值在内存更新，未就绪时明确报错；逐帧结果订阅会话的 ISO/曝光信息变化事件（onIsoInfoChange/onExposureInfoChange 一类）写缓存，会话停止、替换或暂停时清空。
2. 公开 getter 只读内存；UI 访问器、定时器或绘制回调消费控制器值前，看 getter 实现是否含 session./manager. 的同步调用，含则改读缓存。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-d160173a312daca7fc69](../../../../store/cases/case-d160173a312daca7fc69/d91c39d7295c87d4a04f83610561ebe0ef66c0dfd3d09f47323efc62976d0f41.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`d91c39d7295c87d4a04f83610561ebe0ef66c0dfd3d09f47323efc62976d0f41`
