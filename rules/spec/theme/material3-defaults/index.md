# Material3 组件的库默认外观

agent 会看到什么：读到源主题 parent 链到 Theme.Material3.*，界面用 MaterialToolbar、BottomNavigationView、MaterialAlertDialogBuilder、BottomSheetDialogFragment 或 Compose Material3 TopAppBar，没自己写尺寸、底色和留白；规格的设计系统节写「Material3 为基」「Material3 默认」，映射行只写 showAlertDialog / bindSheet

## 通用查法

### 外观来自 Material3 主题和组件默认样式时，规格写出在 Material 库里解析出的具体值

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

## 规矩

- rule-f7ccc76a88df｜规格的设计系统节把 Material3 组件度量写成具体值｜读到：源主题 parent 链到 Theme.Material3.*，界面用 MaterialToolbar、BottomNavigationView；写错：设计系统节只写「Material3 为基、尺寸来自 dimens + Material3 默认」，没写工具栏高度、标题外观、内缩、底栏选中字重和徽标锚点的具体值
- rule-30e93f0ea6fd｜规格写了 M3 组件的默认尺寸时，同一组件的标题 inset 和槽位规则一并写出｜读到：源是 Compose Material3 TopAppBar 等库组件，源码里没有横向 padding，留白来自库的内部布局；写错：规格或验收项写了「TopAppBar 容器高 64vp（Material3 默认）」这类默认值，却没写标题 inset 在哪一侧、导航/动作槽怎么撑开
- rule-0ec19c3e5d27｜规格记录 Material3 主题基底时，一并写出对话框与底部面板的圆角、底色、宽度、遮罩契约｜读到：源工程 styles.xml 的应用主题继承 Theme.Material3.*，源码用 MaterialAlertDialogBuilder、BottomSheetDialog；写错：设计文档主题系统节只记了 Material3 继承树，没有对话框和底部面板的圆角、底色、宽度、遮罩数值；页面规格的映射行只写「MaterialAlertDialog → showAlertDialog / CustomDialog」，不引用外观契约
- rule-85dbe4f0ec1f｜Material3 BottomSheet 页面的规格补记库默认底色和底部系统栏内边距｜读到：源端是 Material3 主题下的 BottomSheetDialogFragment（默认样式 Widget.Material3.BottomSheet），布局没自己写背景和底部内边距；写错：规格没写弹层底色和底部系统栏内边距；或写“Sheet 自身避让系统栏”，按弹层页跳过安全区处理
- rule-44677747ab3b｜源用 M3 small TopAppBar 时，规格写明源码里看不到的默认度量｜读到：Compose 源码只有 TopAppBar(title = …, navigationIcon = …)，没写高度和内边距；写错：页面规格没写顶栏容器高、水平内边距、导航图标和标题起点，或写成 56 高、把状态栏 inset 算进顶栏高度
