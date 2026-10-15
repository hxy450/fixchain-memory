# 手写 %1$s 位置参数插入时字面插入，不把用户数据作为 String.replace 的替换串

ID：`lesson-ecbaa1723e2beb9b1aec` · 版本：3

[本主题](index.md)

## 何时使用

实现阶段，把 Android getString(resId, args) 或 String.format 的 %1$s、%s 位置参数改写为 ArkTS 字符串拼装（自写 formatRes 一类 helper）时

## 适用情境

源端 getString(R.string.x, name) 把用户输入的名称、标题插入格式串（如克隆名后缀）；目标取到格式串后准备用 s.replace('%1$s', arg) 替换占位，或复用兄弟页面已有的同类 helper。

## 原因

JS 的 String.replace 会解释替换串里的 $$、$&、$`、$' 等模式，参数含这些字符时插入结果与原文不同；Android 的 getString 按字面插入参数。

## 做法

1. 占位用 s.split('%1$s').join(arg) 或 s.replace('%1$s', () => arg)（回调返回值不做模式解释）字面插入。也可直接用带格式化参数的重载 resourceManager.getStringSync(resId, ...args)（@ohos.resourceManager.d.ts），不再手写插入。
2. 复用工程已有的格式化 helper 前，核对它是否把参数当替换串插入，是就一并改正。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, recommendation:2
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
