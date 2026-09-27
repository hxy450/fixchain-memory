# 自定义 View 上的 android:* 属性只有被该类读取才生效：控件初值取运行时生效值

ID：`lesson-a6edef3bb44e01a82b72` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时

## 适用情境

源布局在继承 View 的自定义控件（非 CheckBox/CompoundButton）上声明 android:checked 等框架属性，该类构造只读取自己的 styleable 属性；目标用状态变量表示勾选或开关的首显状态。

## 原因

框架属性写在自定义 View 上不会自动生效；照 XML 声明值设初值，首显状态会与 Android 实机相反。联调时若只对照 XML，还会把真实的复刻缺陷误记为“用户例外”。

## 做法

1. 转写自定义 View 的属性前查它的继承链和构造/init 实际读取的属性；未被读取的 android:* 属性不影响运行时，初值取字段默认值以及显示前的 setChecked 等调用。
2. 在注释里分开写“XML 声明值”和“运行时生效值”，依据写到读取该属性的代码行。
3. 用户描述与源 XML 不一致时，先核源控件的运行语义，再决定记为复刻缺陷还是新要求。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-c1b719dc488b73e382db · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`1fc8a39c8b38015c15c4937dee9cd4694ee1c1fdd86fcf886deef6273b16f098`
