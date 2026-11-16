# 外观由 android:Theme.* 平台主题提供时，规格写出在 SDK 平台资源里解析出的值和出处

审的是：规格
触发（任一种）：
- 读到：源控件没写 android:background、textColor、textColorHint 等外观属性，或只写 textAppearance*；应用主题 parent 链止于 android:Theme.Holo / Material / DeviceDefault；写错的样子：规格的转换决策行写「Holo 下划线样式」「暗底白字」「平台默认」「取不到精确值处标待核」，没有具体值、各状态和查过的资源文件
适用范围：由 Android 平台主题提供外观的控件，规格写转换决策行和决策台账时
做法：
- 顺着应用主题的 parent 找到 android:Theme.*；控件样式用到的主题属性（如 editTextBackground、textColorPrimary）到 SDK 平台资源 themes_*.xml 里该主题的条目取引用
- 引用顺着 drawable 或 color 选择器（各状态项；文字色取默认项）、colors_*.xml、styles.xml 读到值，写进该控件的决策行，各状态、内边距、高度一并写
- 只有带资源文件锚点的值标查证；查过仍缺的才标待核，并写明查过哪些文件
针对本应用要查的：
- 应用主题止于哪个平台主题、自己覆盖了哪些项：源工程 AndroidManifest 的 android:theme 和 res/values*/styles.xml，顺着 parent 找到 android:Theme.*；主题自己覆盖了的项取覆盖值，没覆盖的到平台资源里解析
- 平台主题对这一项的值：按应用的 compileSdk 取对应平台的 Android SDK 平台资源 data/res/values/ 下 themes_*.xml、styles.xml、colors_*.xml，以及 data/res/drawable、data/res/color 下的选择器；按主题名和属性名找 item，顺着 @drawable/、@color/、?attr/ 引用读到最终值；例：Theme.Holo 下 textColorPrimary 经 primary_text_holo_dark 的默认项解析到 #F3F3F3
未核实：本族规矩只核对了 android-35 平台资源，别的 compileSdk 下同一主题的取值没逐项比
来源：3 张卡，2 个应用
- case-0ce95f901f7e409784a3（Blockinger）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-20015832edaeb45f53bb（Bubble Shooter）：做法第 3 步 ← 建议 2
- case-e6fd5f0c4d37710c1d97（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
