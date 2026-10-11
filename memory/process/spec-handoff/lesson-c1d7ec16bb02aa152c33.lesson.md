# 规格提取读取 AndroidManifest 的 activity 声明，把窗口级属性写成验收条目

ID：`lesson-c1d7ec16bb02aa152c33` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，为每个 Activity 整理全屏、方向等窗口行为时

## 适用情境

窗口方向（如 screenOrientation=sensorLandscape）只声明在 AndroidManifest，Java 源码只见全屏标志一类调用；页面规格模板与元数据可能没有方向字段。

## 原因

只读 Java 源码会漏掉 manifest 属性；规格与页面元数据都没有方向字段时，实现者会以“规格未覆盖”跳过。

## 做法

1. 为每个 Activity 读 manifest 声明；sensorLandscape 写成“进入页 setPreferredOrientation(AUTO_ROTATION_LANDSCAPE)、离开恢复”的验收条目。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:1
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
