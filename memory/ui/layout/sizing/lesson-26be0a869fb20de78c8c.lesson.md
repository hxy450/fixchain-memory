# Compose Modifier.border 只绘制不改尺寸；ArkUI 容器不设宽高时 .border() 计入测量，先定盒尺寸再画描边

ID：`lesson-26be0a869fb20de78c8c` · 版本：1

[本主题](index.md)

## 何时使用

规格映射与界面实现阶段，把 Compose Modifier.border、drawBehind 等只绘制、不改测量的修饰符落到 ArkUI 容器时

## 适用情境

源 border 画在调用方已定尺寸（Modifier.size 等）的盒内侧，不改变盒尺寸；目标 Stack/Column 自身不设宽高、尺寸由 @BuilderParam 等槽内容决定，准备直接在该容器上写 .border()。

## 例外与边界

- 目标容器已有显式宽高时，.border() 画在该尺寸内、不改变盒尺寸，可以直接写

## 原因

ArkUI 容器未设宽高时，.border() 的宽度计入容器测量（设备 dump 实测），盒子比内容大出描边宽度，后续卡片随之错位；Compose 的 Modifier.border 只在已定尺寸的盒内绘制。

## 做法

1. 先写明目标盒尺寸由谁决定：能拿到调用方尺寸就把宽高提升到带描边的节点上，再写 .border()。
2. 尺寸只能由内容决定时，不在该容器上写 .border()：改用按 onSizeChange 回读的数值宽高叠一层 position({ x: 0, y: 0 }) + hitTestBehavior(HitTestMode.None) 的描边层（首帧会缺描边），规格验收写明“描边不改变盒尺寸”。

## 可选检查

- 有疑问时用 dumpLayout 核对带描边容器的 bounds 与内容子项一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-77c4d0c99ad4a6486b79](../../../../store/cases/case-77c4d0c99ad4a6486b79/0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4`
