# vector 根带 android:tint 时，烘焙进每个可见 path 的 fill，字面色也换

审的是：资源
触发（任一种）：
- 读到：<vector> 根写了 android:tint（如 @color/control_checkable_material），path 的 android:fillColor 是字面 #FF000000，另有 android:fillAlpha="0" 的动画用 path；写错的样子：输出 SVG 的可见 path 仍是 fill="#000000"，只有以 @ 或 ? 开头的 fillColor 换成了解析色；映射表登记的颜色和文件里的 fill 不一致
适用范围：资源迁移阶段把框架或应用的 VectorDrawable 转成 SVG 并烘焙主题 tint 时
做法：
- 根上有 android:tint 时按 tint 链解析出颜色，替换每个可见 path 的 fill（字面 fillColor 也换）；fillAlpha 为 0 的 path 保持透明；多态资源每个状态文件各自烘焙该状态的解析色
- 写映射表前逐个读回输出 SVG 的 fill，与登记的解析色比对，不只抽查一两个文件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Drawable.DEFAULT_BLEND_MODE = BlendMode.SRC_IN，VectorDrawable 的 tint 默认按它混合：SRC_IN 用 tint 色替换所有可见像素的颜色、保留透明度，所以字面 fillColor 也会被 tint 覆盖（出处：android.graphics.drawable.Drawable#DEFAULT_BLEND_MODE；android.graphics.drawable.VectorDrawable#inflate）
- control_checkable_material：state_enabled=false → colorControlNormal（乘 disabledAlpha）；state_checked=true → colorControlActivated；其余 → colorControlNormal：复选框和单选框向量根上的 tint 按状态取色（出处：Android SDK 平台资源 data/res/color/control_checkable_material.xml（按应用的 compileSdk 取对应平台））
- colorControlActivated → ?attr/colorAccent；colorControlNormal → ?attr/textColorSecondary：Material 主题下两个控件色的来源（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 colorControlActivated / colorControlNormal（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题下 colorAccent、textColorSecondary 的实际值：源工程 res/values 下的主题和样式 XML，从 Activity 或应用主题沿 parent 链找到提供这两个属性的那一项；没覆盖时再到 Android SDK 平台资源 values/themes_material.xml 里找；顺着 ?attr、@color 引用解析到具体颜色和透明度，checked 文件用 colorControlActivated 的解析色，unchecked 文件用 colorControlNormal 的解析色（带透明度时写 fill-opacity）
未核实：卡里读的是 android-30 的平台 drawable，本机按 android-36 核对
来源：1 张卡，1 个应用
- case-cec44d314b1979a41843（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
