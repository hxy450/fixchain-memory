# 工具栏菜单项按实际生效的 showAsAction 分流到图标位或溢出菜单（AppCompat 下 android:showAsAction 被忽略；框架 ActionBar 的 withText 只在窗口宽≥480dp 时显示文字），可勾选项开启勾选指示；返回箭头只在源端启用 Up 时绘制

ID：`lesson-a6121cc7eaf207b702f7` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，转换工具栏菜单 XML、自绘 ActionBar 或标题栏，决定图标位、溢出菜单与返回箭头时；自绘框架主题提供的 ActionBar（应用图标、Up 尖角、溢出按钮、横竖屏高度与标题字号）时

## 适用情境

源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。也包括 Activity 基于 AppCompat、菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"），Manifest 没有 parentActivityName、代码没有 setDisplayHomeAsUpEnabled；目标套用自带返回箭头的标题栏模板或兄弟页标题栏。 也包括框架 ActionBar（Theme.Holo 等）带 manifest android:icon、setDisplayHomeAsUpEnabled 与 showAsAction="ifRoom|withText"，目标多个页面各自用 hideTitleBar 自绘标题栏。

## 原因

全部放进溢出菜单或只设选中态，会丢掉工具栏图标位与勾选指示。反过来，AppCompat 只读 app: 命名空间的 showAsAction，android:showAsAction 被忽略、所有项进右上 ⋮ 溢出菜单；把这些项做成标题栏图标，或照模板加返回箭头，都会多出源端没有的入口。框架 ActionBar 的 withText 由 values-w480dp 的 config_allowActionMenuItemTextWithIcon 控制，竖屏窄屏只显示图标；ActionBar 高度与标题字号另有 values-land 取值，图标位显示 manifest 的 Activity 或应用图标。凭记忆总显示文字、省略图标、用字符或折线画 Up 箭头，各页标题栏还各不相同。

## 做法

1. 生效的 showAsAction（AppCompat 读 app:showAsAction，框架 ActionBar 读 android:showAsAction）含 ifRoom/always 且有图标的项放工具栏图标位，仅 never/collapseActionView 的进溢出；checkable 项显式开启 selectIcon 等勾选指示。框架 ActionBar 的 withText 项只在窗口宽 ≥480dp 时在图标旁显示 TextAppearance.Holo.Widget.ActionBar.Menu 文字（12sp 粗体全大写），竖屏窄屏只显示图标。
2. Activity 基于 AppCompat 而菜单写 android:showAsAction 时，该属性被忽略，全部项进右上 ⋮ 溢出菜单，不转成标题栏图标或 NavDestination 图标菜单。
3. 自绘 ActionBar 前查 Manifest 的 parentActivityName 与代码中的 setDisplayHomeAsUpEnabled、getSupportActionBar：都没有就不画返回箭头，返回交给系统返回键与手势；复用模板或兄弟页标题栏前先按当前源核对返回箭头与菜单形态。
4. 自绘框架 ActionBar 时多页共用一个标题栏组件，各页只传图标、标题、是否 Up 与动作项：显示该 Activity 或 application 的 manifest android:icon，Up 尖角与溢出按钮用平台原图（如 ic_ab_back_holo_dark_am、ic_menu_moreoverflow_normal_holo_dark），高度、背景与标题字号取平台样式及 values-land 覆盖值，随窗口尺寸切换。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-5f607109511beae4aec1](../../../store/cases/case-5f607109511beae4aec1/8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772.json) · 结论：recommendation:1, recommendation:3, recommendation:4, recommendation:6
  卡片版本：`8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772`
- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:5
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:4, recommendation:5
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
