# Android 矢量 drawable 转成 SVG 媒体资源再引用，不删掉改用字符代替

审的是：资源
触发（任一种）：
- 读到：源控件 android:src / android:background 引用的 drawable 是 <vector>（带 android:pathData）；写错的样子：目标删掉复制来的矢量 XML，改用「⌫」之类字符；resources/base/media 里没有对应的 .svg
适用范围：源端图标是 Android VectorDrawable、目标需要同一图形时
做法：
- 把 <vector> 的 android:pathData 转成 SVG 的 <path d="…">（viewBox 取 viewportWidth / viewportHeight），存成 resources/base/media 下的 .svg，用 Image($r('app.media.<名>')) 引用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SVG（.svg）：media 资源支持的图片格式之一（出处：resource-categories-and-access.md，媒体资源类型说明）
来源：1 张卡，1 个应用
- case-639b36918b1cd5c1bbe8（android-train-ticket-vest7）：做法第 1 步 ← 建议 5、诊断
