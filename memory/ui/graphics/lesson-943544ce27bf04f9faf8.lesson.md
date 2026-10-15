# 源布局引用的 @drawable 图标在目标判缺失前检索全部限定词目录，缺图从源仓或主题提供方复制原图，不用近名图、符号或纯色底替代

ID：`lesson-943544ce27bf04f9faf8` · 版本：7

[本主题](index.md)

## 何时使用

页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时

## 适用情境

资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里有外观相近、名称相近的其他模块图标。也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标，现有代码用 SymbolGlyph 或 Unicode 字形占位。也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者准备用 Polyline、Circle 或字形自绘。

## 例外与边界

- 源端用文字字符或 emoji 充当图形（Text 或 TextView 显示的字符）：按源字面字符用 Text 实现，不属资源查找
- 主题 parent 链不止于 android:Theme.*（如 AppCompat、MaterialComponents 主题）：本条的 SDK 平台 drawable 路径不适用，按该主题实际所在的依赖库资源查找原图

## 原因

只在 base/media 查找会把已迁移的资源判为缺失，写者随之用字形、品牌色底或外观相近的通用图标代替，截图修复时按视觉相似挑图也会延续偏差。缺图时用近名资源、系统符号或二次着色去模仿原图，会改变图形与颜色。主题或框架控件提供的图标不在应用 res 里，容易被判为“平台 chrome、无源图”而改用自绘图形。

## 做法

1. 判断资源可用性时检索 resources 下全部限定词目录（base、xldpi、dark 等）或按资源映射表核对；构建日志里的“does not have a base resource”说明文件在限定词目录，不是缺失。
2. 图标与装饰图按源布局的 src、drawableStart、background 中的 drawable 名取用，写完按源布局的 drawable 清单逐项对照组件中的引用；头图带透明边缘时，其下的底色取页面背景，不填品牌色。
3. 源图在目标 media 缺失时，先从 Android 仓库对应密度目录（如 drawable-xxhdpi）复制原图并引用（重名时加模块前缀）。不拿其他模块同类、近名或带序号后缀的图标顶替，也不因缺图把“图标 + 文字”结构降成纯文字。
4. 应用 res 里没有、由主题或框架控件提供的图标，先沿 styles.xml 的 parent 链确认提供方：止于 android:Theme.*（框架主题）时，从本机 SDK platforms/android-<api>/data/res/drawable-<密度> 复制原图。不用 Polyline、Circle 或字形自绘平台图标。
5. 源调用点或主题对图标着色（tint、状态选择器）时按源着色保留；原图自带颜色且源端没有 tint 时不再 fillColor 二次着色，替代图颜色不对时先确认是否选错资源。
6. 源仓、SDK 平台 res 与依赖库都找不到时才登记资源缺口，写明查过的目录。现有代码里对应 Android 位图的 SymbolGlyph 或 Unicode 占位要换成原图，只改颜色或字号不算对齐；交付记录写明每个资源来自 Android 原图复制还是工程既有资源，不把近名资源称作原图。

## 可选检查

- 怀疑资源被替换时，用文件大小或哈希比对工程资源与 Android 原图是否一致。

来源支持：5 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-2dbd641ac7d3e926cda7](../../../store/cases/case-2dbd641ac7d3e926cda7/9f617e179563730555fd922a4b1eccc176fed019e9f14bd83673232fa8e40888.json) · 结论：recommendation:3
  卡片版本：`9f617e179563730555fd922a4b1eccc176fed019e9f14bd83673232fa8e40888`
- [case-5f607109511beae4aec1](../../../store/cases/case-5f607109511beae4aec1/8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772.json) · 结论：diagnosis, recommendation:7
  卡片版本：`8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772`
- [case-9394dee6fa8ae478e54c](../../../store/cases/case-9394dee6fa8ae478e54c/8f48c8a73faee7c349509f2ad5bba1c58becb664c51aa5d0652abab5e9df4995.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`8f48c8a73faee7c349509f2ad5bba1c58becb664c51aa5d0652abab5e9df4995`
- [case-cdc57384e71fa7c70345](../../../store/cases/case-cdc57384e71fa7c70345/037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7.json) · 结论：diagnosis, recommendation:1
  卡片版本：`037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7`
- [case-d827908975df4e90ae2b](../../../store/cases/case-d827908975df4e90ae2b/3a1473debde2f4a16a58728c1585a9683b0c44be2bd9aaf8fdaf26b2db0fb492.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3a1473debde2f4a16a58728c1585a9683b0c44be2bd9aaf8fdaf26b2db0fb492`
