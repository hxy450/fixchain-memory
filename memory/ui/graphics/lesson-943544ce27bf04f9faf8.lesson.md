# 图标按源端原始资源与外形落实：检索全部限定词目录，缺失就从 Android 密度目录复制原图，主题或框架控件提供的图标（Up 尖角、溢出、复选框）从 SDK 平台 drawable 复制；不用文字字形、近名图标、系统符号、二次着色或纯色底替代

ID：`lesson-943544ce27bf04f9faf8` · 版本：5

[本主题](index.md)

## 何时使用

页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时；规格提取阶段为源端图标与界面字符写转换决策时

## 适用情境

资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。 也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标（如带 1/2 后缀的阅读器图标），现有代码用 SymbolGlyph 或 Unicode 字形占位，或工程 skill 要求图标优先用已验证的系统 symbol；以及源端用粗体文字字符（“-”“+”）充当按钮图形。也包括源端 Text 直接显示 emoji 字符（如 ⭐、☕️），规格或写者按“不把 emoji 塞进 Text 当图标”一类 symbol 规则改成 SymbolGlyph。 也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者以“平台 chrome、应用无源图”为由用 Polyline、Circle 或字形自绘。

## 原因

只在 base/media 查找会把已迁移的资源判为缺失，写者随之用 Text('人')、Text('›') 之类字形、品牌色底或外观相近的通用图标代替，头像、箭头、提醒图标和透明波浪头图的收口都与源端不符；截图修复时按视觉相似挑图也会延续偏差。来源中页面转换者读到源布局列出的全部 drawable 名，只核对 base/media 就把四个资源判为不存在，改成字形占位并在透明头图下垫了品牌色；返修又从通用资源里挑近似图标。 缺图时用近名资源、系统符号或 fillColor 着色去模仿原图，同样会改变图形、线宽与颜色；skill 的“只用已验证 symbol 名称”约束的是名称合法，不保证外形与源端一致。另一应用中写者已读到规格列出的原图名并查到目标缺图，仍改用另一模块的近名图标加黄色着色，交付时称其为原图；同一应用的步进器把文字“-”换成带圆圈的 minus_circle，另一页的菜单与批量底栏在缺图时直接写成纯文字。

## 做法

1. 判断资源可用性时检索 resources 下全部限定词目录（base、xldpi、dark 等）或按资源映射表核对；构建日志里的“does not have a base resource”说明文件在限定词目录，不是缺失。
2. 图标与装饰图按源布局的 src、drawableStart、background 中的 drawable 名取用，写完按源布局的 drawable 清单逐项对照组件中的引用；确认缺失时登记资源缺口，不以文字字形、纯色底或外观近似的图标替代。
3. 头图带透明边缘时，其下的底色取页面背景，不填品牌色。
4. 源图在目标 media 缺失时，从 Android 仓库对应密度目录（如 drawable-xxhdpi）复制原图并引用（重名时加模块前缀），或登记资源缺口；应用 res 里没有、由主题或框架控件提供的图标，从本机 SDK platforms/android-<api>/data/res/drawable-<密度> 复制原图。不拿其他模块同类、近名或带 1/2 后缀的图标顶替，不用 Polyline、Circle 或字形自绘平台图标，也不因缺图把“图标 + 文字”结构降成纯文字。
5. 原图自带颜色时不再 fillColor 二次着色；替代图颜色不对时先确认是否选错资源。现有代码里对应 Android 位图的 SymbolGlyph 或 Unicode 占位要换成原图，只改颜色或字号不算对齐；交付记录写明每个资源来自 Android 原图复制还是工程既有资源，不把近名资源称作原图。
6. 源端用文字字符充当按钮图形或直接显示字符（粗体“-”“+”、Text 中的 emoji）时按原字符用 Text 实现（短横也可用 Divider/Rect 画同形），symbol 库没有同形名称时不选外形不同的近似 symbol（如 minus_circle）；“只用 symbol、不把 emoji 当图标”一类规则约束的是源端矢量图标资源的映射，与源端字面字符冲突时在规格中记录，不替换。

## 可选检查

- 怀疑资源被替换时，用文件大小或哈希比对工程资源与 Android 原图是否一致。

来源支持：7 张卡 · 5 次迁移 · 5 个应用

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, recommendation:6
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-2dbd641ac7d3e926cda7](../../../store/cases/case-2dbd641ac7d3e926cda7/9f617e179563730555fd922a4b1eccc176fed019e9f14bd83673232fa8e40888.json) · 结论：recommendation:3
  卡片版本：`9f617e179563730555fd922a4b1eccc176fed019e9f14bd83673232fa8e40888`
- [case-5f607109511beae4aec1](../../../store/cases/case-5f607109511beae4aec1/8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772.json) · 结论：diagnosis, recommendation:7
  卡片版本：`8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772`
- [case-6ba16d2344b52f8fca51](../../../store/cases/case-6ba16d2344b52f8fca51/3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f`
- [case-9394dee6fa8ae478e54c](../../../store/cases/case-9394dee6fa8ae478e54c/8f48c8a73faee7c349509f2ad5bba1c58becb664c51aa5d0652abab5e9df4995.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`8f48c8a73faee7c349509f2ad5bba1c58becb664c51aa5d0652abab5e9df4995`
- [case-cdc57384e71fa7c70345](../../../store/cases/case-cdc57384e71fa7c70345/037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7.json) · 结论：diagnosis, recommendation:1
  卡片版本：`037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7`
- [case-d827908975df4e90ae2b](../../../store/cases/case-d827908975df4e90ae2b/3a1473debde2f4a16a58728c1585a9683b0c44be2bd9aaf8fdaf26b2db0fb492.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3a1473debde2f4a16a58728c1585a9683b0c44be2bd9aaf8fdaf26b2db0fb492`
