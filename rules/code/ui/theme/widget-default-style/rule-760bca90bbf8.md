# ImageButton 没写背景时先沿主题解析默认背景，没显式写透明就补按钮底

审的是：代码
触发（任一种）：
- 读到：ImageButton 没写 android:background 和 style，应用主题父链止于 android:Theme.Material（或 Theme、Theme.Holo）；写错的样子：目标写成 Row { Image } 或裸 Image，只加 .stateStyles({ pressed: … }) 按压色，没有静态按钮底和 inset
适用范围：把没写背景的安卓 ImageButton 一类框架控件迁成 ArkUI 组件时
做法：
- 到 Android SDK 平台资源沿生效主题的 imageButtonStyle → 该 style 的 background → drawable 逐级解析；只有源端显式写了 ?attr/selectableItemBackground(Borderless) 才是无底涟漪
- 按解析结果补齐：外层留 inset，内层圆角底色，用 .stateStyles({ normal: {…}, pressed: {…} }) 让整个按钮区按下变色；同类控件做成共享组件复用
- 规格没写默认外观时按源端实际渲染补，并在转换报告里列为规格分歧
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- btn_default_material = <ripple android:color="?attr/colorControlHighlight"> 包 @drawable/btn_default_mtrl_shape：Material 主题下 ImageButton 的背景：涟漪包着一个按钮形状（出处：Android SDK 平台资源 data/res/drawable/btn_default_material.xml（按应用的 compileSdk 取对应平台））
- btn_default_mtrl_shape：左右 inset button_inset_horizontal_material = 4dp、上下 button_inset_vertical_material = 6dp；圆角 buttonCornerRadius = 2dp；tint colorButtonNormal；内距左右 8dp、上下 4dp：按钮底的几何：外层 inset、内层圆角底和形状内距（出处：Android SDK 平台资源 data/res/drawable/btn_default_mtrl_shape.xml；data/res/values/dimens_material.xml，button_inset_*_material、control_corner_material（按应用的 compileSdk 取对应平台））
- Theme.Material.Light 的 colorButtonNormal = @color/btn_default_material_light → button_material_light #ffd6d7d7：浅色 Material 主题下的按钮底色（出处：Android SDK 平台资源 data/res/values/themes_material.xml，colorButtonNormal；data/res/values/colors_material.xml，button_material_light（按应用的 compileSdk 取对应平台））
- Theme.Material.Light 下实测常态 #D6D7D7、按下稳态 #C4C4C4；改成外层 inset 4/6、内层 2dp 圆角底、整区按下变色后与源端一致：修好的写法和对照取值（出处：卡里修好并验证过）
- stateStyles(value: StateStyles): T；StateStyles 有 normal、pressed 等：常态和按下态分别写底色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.stateStyles、StateStyles）
针对本应用要查的：
- 生效主题下的按钮底色、涟漪色和圆角：Android SDK 平台资源 data/res/values/themes_material.xml 里生效主题的 colorButtonNormal、colorControlHighlight、buttonCornerRadius；顺着 @color / @dimen 引用到 res/color、colors_material.xml、dimens_material.xml 读出值；例：Theme.Material.Light 下常态底是 #ffd6d7d7
未核实：按下稳态 #C4C4C4 是实测值，没有按 ripple_material_light 的透明度推算核对
来源：1 张卡，1 个应用
- case-7a330965390c15e18f91（Sokoban）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 4 ← 诊断
