# 手写 getString/String.format 的位置参数插入时，不把用户数据作为 String.replace 的替换串：用 split/join 或替换回调字面插入

ID：`lesson-ecbaa1723e2beb9b1aec` · 版本：2 · 阶段：execute · 主题：[arkts/java-stdlib](index.md)

概要：位置参数插入用 split/join，不把参数当替换串

信号：`getString`, `String.format`, `%1$s`, `String.replace`, `resourceManager.getStringSync`, `formatRes`

## 何时使用

实现阶段，把 Android getString(resId, args) 或 String.format 的 %1$s、%s 位置参数改写为 ArkTS 字符串拼装（自写 formatRes 一类 helper）时

## 适用情境

源端 getString(R.string.x, name) 把用户输入的名称、标题插入格式串（如克隆名后缀）；目标取到格式串后准备用 s.replace('%1$s', arg) 替换占位，或复用兄弟页面已有的同类 helper。

## 原因

JS 的 String.replace 会解释替换串里的 $$、$&、$`、$' 等模式，参数含这些字符时插入结果与原文不同；Android 的格式化按字面插入参数。

## 做法

1. 字面插入：s.split('%1$s').join(arg)，或 s.replace('%1$s', () => arg)（回调返回值不做模式解释）；格式串有多个占位时按序号逐个处理。若本地 SDK 声明提供带格式化参数的取串接口（如 resourceManager.getStringSync(resId, ...args)），可直接用它。
2. 复用工程已有的格式化 helper 前，核对它是否把参数当替换串插入，是就一并改正。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [带 setView 或图标的对话框改用自定义弹窗](../../ui/dialog/carriers/lesson-18fca50f9c801cb282ec.lesson.md)（共享 1 张卡）
- [编译修复只改报错行，不删功能或换异义替代](../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [remember 按首次或 key 变才求值](../../ui/state/lifecycle/lesson-3b4a96141329db62a6af.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../../app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3b8b620c1c7fa2848a34](../../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, rec-208bafcc0d
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
