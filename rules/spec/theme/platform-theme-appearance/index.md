# 平台主题 android:Theme.* 提供的控件外观

agent 会看到什么：读到源控件没写 android:background、textColor 等外观属性，应用主题 parent 链止于 android:Theme.Holo / Material / DeviceDefault；规格的转换决策行和决策台账写「Holo 下划线样式」「暗底白字」「待核」「查证回执」

## 通用查法

### 外观由 android:Theme.* 平台主题提供时，规格写出在 SDK 平台资源里解析出的值和出处

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

## 规矩

- rule-23f1624b25ee｜主题提供控件外观时，规格的决策行写出提供方资源、各状态、内边距和高度｜读到：源控件没写 android:background 等样式属性，应用主题父类是 android:Theme.Holo / Material / DeviceDefault；写错：规格的转换决策行只写“Holo 下划线样式”“取不到精确值处标待核”，没写提供方资源、各状态外观、内容内边距和高度
- rule-379448cfe28c｜styles 父链止于平台主题时，规格里的文字色先在 SDK 平台资源解析到值，不写「暗底白字」｜读到：源 styles 的 parent 链止于 android:Theme.Holo / Theme.Material / Theme.DeviceDefault，文字控件只写 textAppearanceLarge / Medium / Small，或既不写 textColor 也不写 textAppearance；EditText 没写 textColorHint；写错：规格写「文字色（Theme.Holo 暗底白字）| 显式 .fontColor('#FFFFFF')」这类概括，或把次色、提示色写成半透明白并标「待核」
- rule-262423b20079｜裁定来源冲突时只有带资源文件锚点的结论标「查证」，台账依据栏只写打开过的文件｜读到：几条来源对同一外观说法冲突：参考文档里没有锚点的句子、经验提醒；写错：决策台账的依据栏写某布局「查证回执」，但读过的东西里没有打开过这个文件；或者把参考文档里没有锚点的句子当成查证；或者判为误记的来源里另一些片段（如「按钮条右对齐」）未经核对仍留在契约里
- rule-a6cd350e13b3｜控件 style 引用 @android:style/… 时，规格按平台资源写各状态背景和内边距，不凭记忆写透明｜读到：布局里 Button / ImageButton 写 style="@android:style/Widget.ImageWell" 这类框架样式（或快照的 style-ref 以 @android: 开头），没写 android:background；写错：转换决策写「透明背景无描边」「透明底」「平台默认」，没给出处，也没写按下态和内容内边距
- rule-4ab0226c5a33｜布局里没写 background/style 的框架控件，规格沿主题父链定生效主题，写明默认背景、内距与按压态｜读到：布局里 ImageButton、Button 等框架控件只写 src、padding、margin、onClick，没有 android:background 或 style；写错：规格的转换决策行只写「图标按钮 / Image + onClick」「按压反馈 stateStyles 补」，没有主题默认样式带来的按钮底、背景内距
