# 源端菜单行、按钮由 ImageView 加 TextView 或 drawableLeft 组成时，目标写图标加文字

审的是：代码
触发（任一种）：
- 读到：弹出菜单行、操作按钮由 <ImageView android:src="@drawable/..."> 加 <TextView> 组成，或标题 TextView 带 android:drawableLeft / android:drawableStart 图标和专用 @color 颜色资源；写错的样子：目标的菜单行、操作栏按钮或分组标题只有 Text(...)，没有 Image($r('app.media....'))，文字颜色和字号也不是源端的颜色资源和尺寸
适用范围：界面实现阶段新建菜单、列表分组标题、操作栏等源端由图标和文字组成的入口时，即使差异清单和规格只写了行为
做法：
- 动笔前从源布局 XML（和截图，如有）列出每个可见元素：ImageView、drawableLeft / drawableStart、按状态切换的 drawable、文字字号和颜色资源；编码后逐项对照
- 每行写成 Row() { Image($r('app.media.<源图名>')).width(<源 dp>).height(<源 dp>); Text(...).fontSize(<源 sp>).fontColor($r('app.color.<源颜色名>')) }（上下排的按钮用 Column），行高、宽度照源端 dp
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- drawableLeft、drawableStart 的 format 是 reference|color：TextView 上的左侧 / 起始侧图标，迁移时要成为单独的 Image（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextView 的 drawableLeft / drawableStart（按应用的 compileSdk 取对应平台））
- (src: PixelMap | ResourceStr | DrawableDescriptor): ImageAttribute：Image 的构造，图标用 $r('app.media.名字') 传入（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageInterface）
- 菜单改为 24vp 图标加文字、标题改为图标加专用颜色后，与源端截图一致：修复后的形态（出处：卡里修好并验证过）
针对本应用要查的：
- 每个可见元素的图、尺寸和颜色：源工程的布局 XML 里这一行或按钮的 ImageView 的 android:src、layout_width / layout_height，TextView 的 textSize、textColor、drawableLeft；标题若由单独的 item 布局生成就打开那个布局；图名对应 $r('app.media.图名')，dp 照搬成 vp，sp 照搬成 fp，@color 名对应 $r('app.color.名')
来源：1 张卡，1 个应用
- case-2dbd641ac7d3e926cda7（刺猬猫阅读）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
