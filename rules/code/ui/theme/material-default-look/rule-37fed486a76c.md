# 控件没写 style 时按应用主题父类解析默认外观，不套映射表的 M2 描述

审的是：代码
触发（任一种）：
- 读到：FloatingActionButton 没写 style，应用主题继承 Theme.Material3.*；写错的样子：Button 写成圆形 borderRadius(28)、强调色底、白图标，或按映射表加了硬 .shadow
- 读到：按钮 style 继承 Widget.Material3.Button.OutlinedButton，只覆写了 backgroundTint；写错的样子：按钮文字只设 fontSize 和颜色，没有 fontWeight(FontWeight.Medium)
- 读到：PreferenceCategory 分组标题，主题没改分组标题色；写错的样子：分组标题 fontColor 用 M2 的 textColorSecondary 次要色，不是 colorAccent 对应色
适用范围：源控件没显式写外观属性、外观来自 Material3 主题或 AndroidX Preference 库默认样式时
做法：
- 按「控件 style → 主题里的默认样式属性（如 floatingActionButtonStyle）→ 主题父类」找到提供值的样式，顺着 ?attr/ 解析到颜色、圆角、字重
- Theme.Material3.* 下：FAB 写 borderRadius(16) 方形圆角、底色 colorPrimaryContainer、图标色 colorOnPrimaryContainer；OutlinedButton 文字 14fp + FontWeight.Medium；PreferenceCategory 标题用 colorAccent 对应色
- 通用映射表里「FAB → 圆形 + 阴影」这类 M2 描述，先与主题核对再用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- floatingActionButtonStyle = ?attr/floatingActionButtonPrimaryStyle → Widget.Material3.FloatingActionButton.Primary：Material3 主题下没写 style 的 FAB 取这个样式（出处：com.google.android.material:material 包内 res/values/values.xml，Theme.Material3 的 floatingActionButtonStyle、floatingActionButtonPrimaryStyle（按应用依赖的版本））
- m3_comp_fab_primary_container_shape = ?attr/shapeAppearanceCornerLarge；ShapeAppearance.M3.Sys.Shape.Corner.Large 的 cornerSize = 16dp：FAB 默认是 16dp 圆角方形（material 1.12.0）（出处：com.google.android.material:material 包内 res/values/values.xml，m3_comp_fab_primary_container_shape、ShapeAppearance.M3.Sys.Shape.Corner.Large（按应用依赖的版本））
- m3_comp_fab_primary_container_color = ?attr/colorPrimaryContainer；m3_comp_fab_primary_icon_color = ?attr/colorOnPrimaryContainer：FAB 默认底色和图标色（material 1.12.0）（出处：com.google.android.material:material 包内 res/values/values.xml，m3_comp_fab_primary_container_color、m3_comp_fab_primary_icon_color（按应用依赖的版本））
- OutlinedButton 继承 TextButton，textAppearance = ?attr/textAppearanceLabelLarge → TextAppearance.M3.Sys.Typescale.LabelLarge：sans-serif-medium、14sp：M3 描边按钮文字默认 14sp、Medium 字重（出处：com.google.android.material:material 包内 res/values/values.xml，m3_comp_text_button_label_text_type、TextAppearance.M3.Sys.Typescale.LabelLarge（按应用依赖的版本））
- PreferenceThemeOverlay（v21）：preferenceCategoryTitleTextColor = ?android:attr/colorAccent：分组标题默认用主题的 colorAccent（出处：androidx.preference:preference 包内 res/values-v21/values-v21.xml，PreferenceThemeOverlay（按应用依赖的版本））
- FAB 改成 16 圆角 + primaryContainer 底色 / onPrimaryContainer 图标、按钮文字补 Medium、分组标题改强调色后与源端一致：Material3 主题下这几项默认外观（出处：卡里修好并验证过）
针对本应用要查的：
- 应用主题的父类和覆写：源工程 res/values 下 styles.xml、themes.xml 里清单引用的应用主题，沿 parent 找到 Theme.Material3.* 或 Theme.MaterialComponents.*；看有没有覆写 floatingActionButtonStyle、colorPrimaryContainer、preferenceTheme 等；有覆写取覆写值，没有取库默认
- 所依赖 material 库版本下的默认取值：应用依赖版本的 com.google.android.material:material 包内 res/values/values.xml，按 m3_comp_fab_primary_container_color、m3_comp_fab_primary_container_shape 等宏名找；顺着 ?attr/ 到主题里的颜色值写进目标 color.json；例：1.12.0 下 FAB 底色宏是 colorPrimaryContainer，1.14.0 下改成 colorPrimary
未核实：material 1.14.0 里 m3_comp_fab_primary_container_color 改成 ?attr/colorPrimary，卡里的取值对应哪个库版本没标明
来源：1 张卡，1 个应用
- case-85baa9234cc4f4798784（AntennaPod）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断；做法第 3 步 ← 建议 4；取值 6 ← 诊断
