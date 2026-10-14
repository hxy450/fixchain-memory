# 把主题与默认样式继承的文字外观解析成具体值，并显式设置TextView行高

ID：`lesson-c5f30aef1c67f6891b0b` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为使用textAppearance*或未写textColor的TextView、继承平台默认样式的Button确定字色、字重、大小写、行高与最小尺寸时

## 适用情境

源控件用?android:attr/textAppearance*、依赖应用主题的textColorPrimary，或Button只套了改背景/字色的自定义style（未改其余默认属性）；目标用Text或自组合按钮实现。

## 原因

继承来的属性不出现在布局XML里，只照搬显式属性会丢掉主题字色和Button默认的字重、全大写、最小尺寸；ArkUI Text默认行高比安卓TextView（含includeFontPadding）矮，框高和文字位置随之偏移；背景被换成透明色后，安卓Button也不再有默认内边距。

## 做法

1. 按应用主题链把继承值解析成具体值写进规格：字号、字色（未写textColor时取主题textColorPrimary，AppCompat Light为#DE000000）、字重、textAllCaps、minWidth/minHeight。
2. 解析出一个默认属性后，把同一默认样式的其他属性逐项核完；通用陷阱条目（如“Button有默认padding”）先确认源样式是否替换了背景再用。
3. Text显式设置lineHeight，取值以安卓TextView实测的单行高与行距为准，单位用fp以随系统字号缩放。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-996cb7d3a76b61367794](../../../store/cases/case-996cb7d3a76b61367794/2f02cb9f32c29a0bd5c96f57565ee4cca462f6e35b54831d019a1b2d2f0bf281.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`2f02cb9f32c29a0bd5c96f57565ee4cca462f6e35b54831d019a1b2d2f0bf281`
