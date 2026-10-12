# 规格提取读取 AndroidManifest 的 application 与 activity 声明（含未声明时的平台缺省），把窗口与应用级属性写成验收条目并指派实现

ID：`lesson-c1d7ec16bb02aa152c33` · 版本：2

[本主题](index.md)

## 何时使用

规格提取阶段，为每个 Activity 整理全屏、方向、软键盘等窗口行为，并整理 application 级属性（备份等）时

## 适用情境

窗口方向（如 screenOrientation=sensorLandscape）只声明在 AndroidManifest，Java 源码只见全屏标志一类调用；页面规格模板与元数据可能没有方向字段。也包括 application 显式 allowBackup=false，activity 未声明 screenOrientation、windowSoftInputMode 而依赖平台缺省；界面图谱把它们记为 unspecified/unknown，功能基线与计划都没有对应任务，目标备份配置保持模板值。

## 原因

只读 Java 源码会漏掉 manifest 属性；规格与页面元数据都没有方向字段时，实现者会以“规格未覆盖”跳过。记为 unspecified/unknown 的项没有目标值，下游没有写者，模板默认值（如允许备份）会保留到交付。

## 做法

1. 为每个 Activity 读 manifest 声明；sensorLandscape 写成“进入页 setPreferredOrientation(AUTO_ROTATION_LANDSCAPE)、离开恢复”的验收条目。
2. 逐项列出 application/activity 属性及其缺省语义，映射到备份配置（allowToBackupRestore）、ability 的 orientation 与窗口的 KeyboardAvoidMode 等，并为每项指派实现任务；未声明的项按 Android 缺省语义给出目标值（来源分别落为 auto_rotation_restricted 与 KeyboardAvoidMode.RESIZE），不留 unknown。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:1
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:4
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
