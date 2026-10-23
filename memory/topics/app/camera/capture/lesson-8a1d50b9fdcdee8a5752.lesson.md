# 拍照结果改走无请求 ID 的 photoAssetAvailable 时，按一次拍摄独占一个 PhotoOutput，超时或失败即退役该输出再接受下次拍摄

ID：`lesson-8a1d50b9fdcdee8a5752` · 版本：1 · 阶段：execute/repair · 主题：[app/camera/capture](index.md)

概要：资产回调无请求 ID 时一拍一输出，超时退役不串帧

信号：`photoAssetAvailable`, `PhotoOutput`, `captureStartWithInfo`, `captureEnd`, `captureId`, `PhotoAsset`

## 何时使用

拍照通道实现或返修阶段，把拍照结果接到 photoAssetAvailable 资产回调，并设计超时、失败与下一次拍摄的衔接时

## 适用情境

目标拍照结果经 PhotoOutput 的 photoAssetAvailable 回调交付 PhotoAsset，回调参数里没有本次拍摄的请求或 capture ID；实现用一个结果接收者等待资产，并为单次拍摄设了超时或失败恢复。

## 例外与边界

- 输出串行且每次拍摄都在确认上一张资产到达或输出已重建之后才发起

## 原因

photoAssetAvailable 只交付 PhotoAsset（API 24 @ohos.multimedia.camera.d.ts L7865），captureId 只出现在拍摄开始/结束信息里；超时后只清空接收者、不退役输出，迟到的资产会被下一次拍摄的接收者收下，造成串帧。

## 做法

1. 把“一次拍摄”与“一个 PhotoOutput”绑定：超时或失败时退役该输出（停止接收其回调）并重建会话或输出，恢复完成后再接受下一次拍摄；不要把迟到资产交给当时唯一的结果接收者。
2. 需要关联开始/结束事件时用 captureStartWithInfo / captureEnd 的 captureId 记录在途拍摄，但资产本身无法按 ID 匹配，仍以输出退役为准。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [权限按目标 API 的 @permission 汇总](../../capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md)（共享 1 张卡）
- [相机产出走系统资产保存，不靠受限写权限](../../media-library/lesson-bc279ce222e98e0d5ede.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-58c3f872e3c907fb4b68](../../../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：rec-db04c96a33
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
