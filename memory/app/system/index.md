# app/system

窗口与系统级配置：系统栏、屏幕方向、系统字号跟随

[上一级](../index.md)

## 本级经验

- [源Activity未声明方向且有横屏资源时，声明随传感器旋转的orientation](lesson-67cef60aed25d831cd24.lesson.md)
  - 时机：规格提取与实现阶段，决定目标UIAbility窗口方向声明、实现横竖屏双布局时
  - 情境：源Activity未声明screenOrientation（开启自动旋转时随传感器转屏），并提供layout-land等横屏资源；目标module.json5中EntryAbility未声明orientation。
- [源文字随系统字号缩放时，目标应用声明fontSizeScale跟随系统](lesson-8d44370a5c527870dfb7.lesson.md)
  - 时机：规格决策与应用配置落地阶段，裁定大字体能力、改写app.json5时
  - 情境：源文字使用sp或textAppearance*主题样式（无需代码即随系统字号缩放）；目标AppScope/app.json5未声明configuration。
- [系统栏外观按源主题实际表现设置，横屏时显式显示状态栏](lesson-9f63aee8d01fcad54884.lesson.md)
  - 时机：界面实现阶段，在入口Ability中为全屏页设置窗口布局、系统栏颜色与显隐时
  - 情境：源Activity使用未定制系统栏的标准主题（无translucent、statusBarColor、全屏或SYSTEM_UI标志），目标规格只要求按沉浸式架构实施；源端支持横屏。
  - 例外：源端确实设置了透明或沉浸系统栏、全屏标志时，按源端设置迁移
