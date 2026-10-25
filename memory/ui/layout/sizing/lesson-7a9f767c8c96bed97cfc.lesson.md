# ContentScale.FillWidth 无 ImageFit 对应值：宽度铺满、高按图片比例、容器 clip，不用 Fill/Cover

ID：`lesson-7a9f767c8c96bed97cfc` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose Image/AsyncImage 的 contentScale 映射为 ArkUI Image 属性时

## 适用情境

源端图片用 ContentScale.FillWidth（如模糊缩略图、横幅），或由调用方传入 contentScale；目标 ArkUI Image 只有 objectFit 的 Fill、Cover、Contain 等取值。

## 原因

FillWidth 按宽度等比缩放，高度溢出时居中裁切；Fill 会拉伸变形，Cover 按两轴取大可能裁掉左右。组件只暴露 objectFit 参数时，调用方传 FillWidth 的意图在目标组件里没有入口，只能被就近换成 Fill。

## 做法

1. 宽度铺满容器，高度取容器宽除以图片宽高比（onComplete 拿到图片宽高，onAreaChange 取容器宽），显式尺寸溢出部分由容器 clip 并居中。
2. Android 组件的 contentScale 由调用方传入时，目标组件也提供对应参数（如 fillWidth），不在组件内固定一种 objectFit。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-af4252d474c172e093fc](../../../../store/cases/case-af4252d474c172e093fc/cbb8ea02978ec26f3c0634ccd8741583db0582686b51cc563af4b5a5325614d1.json) · 结论：recommendation:4
  卡片版本：`cbb8ea02978ec26f3c0634ccd8741583db0582686b51cc563af4b5a5325614d1`
