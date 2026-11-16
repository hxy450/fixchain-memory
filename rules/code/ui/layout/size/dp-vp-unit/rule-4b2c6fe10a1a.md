# Image 用 vector drawable 不设尺寸时，目标按 vector 的 dp 尺寸写，不再除以密度

审的是：代码
触发（任一种）：
- 读到：Compose `Image(painterResource(...))` 不设尺寸，资源是 vector drawable，`android:width`/`android:height` 写的是 dp，放在无密度限定的 drawable 目录；写错的样子：目标 `Image` 只写 `objectFit` 没有尺寸，或宽高写成 vector 的 dp 数除以 3（自动修复按回退密度当像素换算）
适用范围：把 Compose 里不设尺寸、按固有尺寸显示的 vector 图迁成 ArkUI Image 时，包括收口阶段自动修复改写图片尺寸后
做法：
- 尺寸直接用 vector 的 dp 数，不做 ÷density；按宽度自适应时写 `.width('100%').constraintSize({ maxWidth: W }).aspectRatio(W / H)`，W、H 是 android:width/height 的 dp 数
- 自动修复改写了图片尺寸时，用源 drawable 的 android:width/height 对照一次；源 drawable 在无密度限定目录时只报告，不按回退密度写回代码
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- VectorDrawable 的 width/height 是它的固有宽高：源端不设尺寸时按这个 dp 值显示（出处：Android SDK 平台资源 data/res/values/attrs.xml，VectorDrawable 的 width/height（按应用的 compileSdk 取对应平台））
- aspectRatio(value: number): T：组件宽高比（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.aspectRatio）
- constraintSize(value: ConstraintSizeOptions): T：约束尺寸，写 maxWidth 限制最大宽度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.constraintSize）
- width('100%') + constraintSize({ maxWidth: W }) + aspectRatio(W / H)：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- vector 图的固有尺寸：源工程 res/drawable*/ 下同名的 vector XML，根元素 <vector> 的 android:width、android:height；读出 dp 数作为 W、H
来源：1 张卡，1 个应用
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 7、诊断；做法第 2 步 ← 建议 7；取值 4 ← 诊断
