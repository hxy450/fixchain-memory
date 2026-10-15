# 自定义 View 上的 android:* 属性只有继承链中某个类读取时才生效：控件初值取运行时生效值

ID：`lesson-a6edef3bb44e01a82b72` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时

## 适用情境

源布局在自定义控件上声明 android:checked、android:enabled 等框架属性，该类直接继承 View（或继承链中没有读取该属性的类），构造只读取自己的 styleable 属性；目标用状态变量表示勾选、开关或可用态的首显状态。

## 原因

框架属性由继承链中对应的类在构造时读取：View 基类读 background、padding、visibility 等，android:enabled 由 TextView 读，android:checked 由 CompoundButton 读（见 SDK sources 中 View.java、TextView.java、CompoundButton.java）。直接继承 View 的自定义控件上写 enabled、checked 不会生效；照 XML 声明值设初值，首显状态会与 Android 实机相反。联调时若只对照 XML，还会把真实的复刻缺陷误记为“用户例外”。

## 做法

1. 转写自定义 View 的属性前查它的继承链，以及链上各类与自身构造/init 实际读取的属性；未被读取的 android:* 属性不影响运行时，初值取字段默认值以及显示前的 setChecked、setEnabled 等调用。
2. 在注释里分开写“XML 声明值”和“运行时生效值”，依据写到读取该属性的代码行。
3. 用户描述与源 XML 不一致时，先核源控件的运行语义，再决定记为复刻缺陷还是新要求。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c1b719dc488b73e382db](../../../store/cases/case-c1b719dc488b73e382db/b10b623ec0dd553442560d133fa27dd9436f685e6e053feb8a5c03353cc2b544.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b10b623ec0dd553442560d133fa27dd9436f685e6e053feb8a5c03353cc2b544`
