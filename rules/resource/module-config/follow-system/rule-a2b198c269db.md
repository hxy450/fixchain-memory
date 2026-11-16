# 安卓缺省跟随系统的设置没写时，查鸿蒙对应配置项的缺省值并显式写跟随

审的是：资源
触发（任一种）：
- 读到：源端没显式写、按安卓缺省跟随系统的行为：AndroidManifest.xml 的 <activity> 没有 android:screenOrientation；文本用 sp，或有 AlertDialog.Builder、Toast；写错的样子：目标 module.json5 的 abilities 条目没有 orientation，或 AppScope/app.json5 没有 configuration（引用的 profile 里没有 fontSizeScale），沿用了鸿蒙的缺省值
适用范围：手机形态的目标工程，把源端缺省跟随系统设置（屏幕旋转、字号）的应用级行为落到 app.json5、module.json5 时
做法：
- 对源端没写的那一项，按安卓缺省认定行为：<activity> 不写 screenOrientation 即 unspecified，随传感器和系统旋转开关旋转；sp 文本、系统对话框随系统字号缩放
- 按配置项名查目标端这一项的取值和缺省值（module.json5 查 abilities 标签，app.json5 查 configuration 标签）；缺省值不跟随系统时，在目标配置里显式写跟随系统的那个取值，不留空沿用缺省
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- orientation 可缺省，缺省值 unspecified（未指定方向，由系统自动判断显示方向）；auto_rotation_restricted：传感器开关打开，方向可随传感器旋转：module.json5 abilities 的方向配置：缺省值，以及跟随系统旋转开关的取值（出处：module-configuration-file.md，abilities标签）
- fontSizeScale：followSystem / nonFollowSystem，缺省 nonFollowSystem；app.json5 里用 "configuration": "$profile:configuration" 引用 profile：应用字号是否跟随系统，缺省不跟随（出处：app-configuration-file.md，configuration标签）
- screenOrientation 的 unspecified：让系统决定；用户没关自动旋转时随设备旋转：源端不写 screenOrientation 时的行为（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，screenOrientation（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源端这一项有没有显式声明：源工程 AndroidManifest.xml 各 <activity> 的 android:screenOrientation、android:configChanges；布局、样式和代码里文本尺寸的单位；没写方向的按 unspecified 算（随系统旋转）；文本用 sp 的按随系统字号算；写了锁定方向的取目标 orientation 枚举里对应的值
- 目标对应配置项的缺省值：OpenHarmony 文档 quick-start 下 module-configuration-file.md 的 abilities 标签、app-configuration-file.md 的 configuration 标签，按配置项名找那一行；读取值说明和缺省值；缺省值不是跟随系统的就要显式写。例：手机形态工程里 EntryAbility 不写 orientation 时，解除旋转锁转 90° 窗口仍不旋转，写 auto_rotation_restricted 后变为横屏（卡里修好并验证过）
来源：2 张卡，2 个应用
- case-a824609ada4969e6d96c（2048）：做法第 2 步 ← 建议 2
- case-c6c056189eaa36176e28（Blockinger）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 2
