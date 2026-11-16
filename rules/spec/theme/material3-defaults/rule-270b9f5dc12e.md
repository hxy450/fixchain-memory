# 外观来自 Material3 主题和组件默认样式时，规格写出在 Material 库里解析出的具体值

审的是：规格
触发（任一种）：
- 读到：源主题 parent 链到 Theme.Material3.*，界面用 MaterialToolbar、MaterialAlertDialogBuilder、BottomSheetDialogFragment 或 Compose Material3 组件，没自己写尺寸、底色、圆角和内边距；写错的样子：规格写「Material3 为基」「Material3 默认」或只写目标接口名，没有组件的高度、圆角、底色、遮罩、内边距等具体值
适用范围：源端组件外观由 Material3 库默认提供，规格写设计系统节、主题系统节和组件映射行时
做法：
- 按组件找它的默认样式：主题里对应的样式属性，或 Widget.Material3.*、MaterialAlertDialog.Material3 一类样式；Compose 组件看 androidx.compose.material3 里的组件实现
- 顺着样式里的 @macro/、?attr/、@dimen/ 读到值；颜色属性再到应用主题或 Theme.Material3 的浅深主题解析出两份
- 规格把这些值写成组件度量和外观契约，组件映射行引用它
针对本应用要查的：
- 组件默认样式和它的取值：应用依赖版本的 com.google.android.material:material 包内 res/values/values.xml，按样式名和 m3_comp_* 的 macro、dimen 名找；顺着 @macro/ 到 ?attr/、@dimen/ 读到值；例：material 1.12.0 下 Widget.Material3.BottomSheet 的 backgroundTint 经 m3_comp_sheet_bottom_docked_container_color 落到 ?attr/colorSurfaceContainerLow
- 应用主题对这些颜色属性的覆写：源工程 res/values 与 values-night 下 themes / styles 里应用主题的 colorSurfaceContainerLow、colorSurfaceContainerHigh 等 item；没覆写时看 Material 库的 Theme.Material3 浅深主题；解析到浅色、深色两个色值，写成已迁移的颜色资源名
未核实：Compose Material3 组件的内部留白，本族规矩没有在库源码里核实
来源：3 张卡，1 个应用
- case-1ff61bb8eea97c7cac7f（AntennaPod）：做法第 1 步 ← 建议 6；做法第 2 步 ← 建议 6
- case-9c819765c4d3d422d7bb（AntennaPod）：做法第 2 步 ← 建议 5；做法第 3 步 ← 建议 5
- case-a3dc4d0187d7ddc456e8（AntennaPod）：做法第 1 步 ← 建议 5；做法第 3 步 ← 建议 5
