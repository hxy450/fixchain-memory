# Material3 BottomSheet 页面的规格补记库默认底色和底部系统栏内边距

审的是：规格
触发（任一种）：
- 读到：源端是 Material3 主题下的 BottomSheetDialogFragment（默认样式 Widget.Material3.BottomSheet），布局没自己写背景和底部内边距；写错的样子：规格没写弹层底色和底部系统栏内边距；或写“Sheet 自身避让系统栏”，按弹层页跳过安全区处理
适用范围：规格提取阶段遇到 Material3 BottomSheet 页面时
做法：
- 规格里补两项：弹层底色 = 库默认 colorSurfaceContainerLow 在应用主题里映射到的已迁移颜色资源；底部内边距 = 内容底部加上系统导航条的高度（对应 paddingBottomSystemWindowInsets），写明 bindSheet 不会自动避让底部导航条
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material3.BottomSheet 的 backgroundTint = @macro/m3_comp_sheet_bottom_docked_container_color = ?attr/colorSurfaceContainerLow：Material3 底部弹层的默认底色（出处：com.google.android.material:material 包内 res/values/values.xml，Widget.Material3.BottomSheet、m3_comp_sheet_bottom_docked_container_color（按应用依赖的版本））
- Widget.Material3.BottomSheet 的 paddingBottomSystemWindowInsets = true：源端弹层内容底部自动加上系统栏内边距（出处：com.google.android.material:material 包内 res/values/values.xml，Widget.Material3.BottomSheet（按应用依赖的版本））
- BindOptions.backgroundColor 默认 Color.White：目标不写底色时是白色，不跟源端主题（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BindOptions.backgroundColor）
针对本应用要查的：
- colorSurfaceContainerLow 在应用主题里的值：源工程 res/values/themes.xml、values-night/themes.xml 里应用主题对 colorSurfaceContainerLow 的定义；没有定义时看应用依赖版本的 material 包内 Theme.Material3 系主题；解析到具体颜色，找目标已迁移的对应颜色资源名写进规格
未核实：卡里没有写前就收到这两项要求的反例，建议出自返修时的补救
来源：1 张卡，1 个应用
- case-1ff61bb8eea97c7cac7f（AntennaPod）：做法第 1 步 ← 建议 6
