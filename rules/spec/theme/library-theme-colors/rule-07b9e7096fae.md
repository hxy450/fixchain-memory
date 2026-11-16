# 源 Button 没写样式、主题是 MaterialComponents 系时，规格按钮行写明底色字色圆角最小高度

审的是：规格
触发（任一种）：
- 读到：源布局里 Button 没写 android:background、backgroundTint、textColor、cornerRadius，应用主题的父主题是 Theme.MaterialComponents.*，设计令牌里有 colorPrimary、colorOnPrimary；写错的样子：规格里这个 Button 的转换决策行只有文案、字号、边距；主题色只在全局写一句“颜色由资源系统负责”或“页面代码零硬编码色值”，按钮行没有底色、字色、圆角
适用范围：规格提取阶段，源布局中没有显式样式、外观由 MaterialComponents 系主题的默认按钮样式提供的 Button
做法：
- 先查应用主题的父主题和语义色，再在该控件自己的转换决策行写出主题带来的外观，用已迁移的颜色资源名表达，如 .backgroundColor($r('app.color.colorPrimary')).fontColor($r('app.color.colorOnPrimary')).borderRadius(4).constraintSize({ minHeight: 48 })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.MaterialComponents.Button 的 backgroundTint 是 @color/mtrl_btn_bg_color_selector，启用态取 ?attr/colorPrimary：按钮底色来自主题的 colorPrimary（出处：com.google.android.material:material 包内 res/values/values.xml，Widget.MaterialComponents.Button；res/color/mtrl_btn_bg_color_selector.xml（按应用依赖的版本））
- Widget.MaterialComponents.Button 的 android:textColor 是 @color/mtrl_btn_text_color_selector，启用态取 ?attr/colorOnPrimary：按钮字色来自主题的 colorOnPrimary（出处：com.google.android.material:material 包内 res/color/mtrl_btn_text_color_selector.xml（按应用依赖的版本））
- shapeAppearance 取 ShapeAppearance.MaterialComponents.SmallComponent，cornerSize = mtrl_shape_corner_size_small_component = 4dp；父样式 Base.Widget.AppCompat.Button 的 android:minHeight 是 48dip：圆角 4、最小高度 48 的来源（出处：com.google.android.material:material 包内 res/values/values.xml，mtrl_shape_corner_size_small_component；androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.Button（按应用依赖的版本））
- ButtonOptions.type 默认 ButtonType.ROUNDED_RECTANGLE（API 18 之前默认 Capsule）：目标 Button 不设样式时用平台默认形状和强调色，不会跟着源主题（出处：ts-basic-components-button.md，ButtonOptions）
- Button 补上 backgroundColor、fontColor、borderRadius(4)、constraintSize({ minHeight: 48 }) 后，复测底色与源主题 colorPrimary 一致：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 主题给按钮的语义色：源工程 res/values/themes.xml 和 values-night/themes.xml 里应用主题的 colorPrimary、colorOnPrimary，以及 parent 链；顺着 @color/… 解析到值；目标已迁移的同名颜色资源就用它的名字写 $r('app.color.…')
- 按钮默认样式的圆角、最小高度：应用依赖版本的 com.google.android.material:material 包内 res/values/values.xml，主题的 materialButtonStyle 指向的样式；读 shapeAppearance 对应样式的 cornerSize 和父样式的 android:minHeight；布局里 Button 若有 style= 或主题覆盖了 materialButtonStyle，以覆盖的样式为准
未核实：卡里的实测出自 HarmonyOS 6.1.1（API 24），本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-97a40a9d2dce65dc9f9c（Dice Roller）：做法第 1 步 ← 建议 1、诊断；取值 5 ← 诊断
