# 源Activity未声明方向且有横屏资源时，声明随传感器旋转的orientation

ID：`lesson-67cef60aed25d831cd24` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与实现阶段，决定目标UIAbility窗口方向声明、实现横竖屏双布局时

## 适用情境

源Activity未声明screenOrientation（开启自动旋转时随传感器转屏），并提供layout-land等横屏资源；目标module.json5中EntryAbility未声明orientation。

## 原因

只把横竖屏映射成响应式布局，窗口能否旋转就无人负责；鸿蒙手机UIAbility未声明方向时不随传感器旋转，横屏布局永远到不了。

## 做法

1. 在module.json5为EntryAbility声明随传感器旋转且受旋转锁控制的orientation（如auto_rotation_restricted），并在台账列为技术必做项。
2. 实现双布局时确认窗口确实会旋转，验收时做一次设备旋转。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4ded9779080f194c96e2](../../../store/cases/case-4ded9779080f194c96e2/2fe8af238707f4e11a9b5ab402f6eba6988194f7e8d5d61864ba4d42d455cc58.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`2fe8af238707f4e11a9b5ab402f6eba6988194f7e8d5d61864ba4d42d455cc58`
