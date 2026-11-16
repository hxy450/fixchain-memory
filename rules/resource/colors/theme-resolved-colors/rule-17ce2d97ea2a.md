# 颜色来自主题或平台、库默认时，浅深主题分别沿 parent 链解析，base 和 dark 各写

审的是：资源
触发（任一种）：
- 读到：源控件颜色引用 ?attr/…、?android:attr/…，或没写 android:textColor、取主题默认；写错的样子：color.json 里是凭记忆的近似值，或 base 和 dark 同值、dark 缺同名键
- 读到：应用主题沿 parent 链止于 Theme.AppCompat.*、Theme.Material3.*、android:Theme.Holo；写错的样子：dark/element/color.json 只镜像 base，或保留脚手架 #FFFFFF / #000000
适用范围：为主题提供的颜色在 base 和 dark 的 color.json 建键时
做法：
- 浅色、深色分别沿 parent 链找第一个写了该属性的 item：应用 values 与 values-night 的 styles.xml → 依赖库包内 res/values*/values*.xml → Android SDK 平台资源 data/res/values/themes*.xml
- 顺着 @color/… 引用解析到色值，浅色写进 base、深色写进 dark 的同名键；查过仍取不到才登记待核，不落近似值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- resources 下建限定词目录 dark，在 base/element/color.json 和 dark/element/color.json 里定义同名颜色、赋不同的值：深色模式下 $r('app.color.<同名键>') 取 dark 里的值（出处：ui-dark-light-color-adaptation.md，应用跟随系统的深浅色模式）
- 先在匹配设备状态的限定词目录里找，找不到才去 base：dark 里缺这一项时深色模式下用 base 的浅色值（出处：resource-categories-and-access.md，资源匹配）
- Theme.Material.Light：windowBackground = ?attr/colorBackground，colorBackground = @color/background_material_light = @color/material_grey_50 = #fffafafa：例：AppCompat Light 系主题没覆盖时窗口底色的解析链（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light；data/res/values/colors_material.xml，background_material_light、material_grey_50（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 这个颜色在浅色、深色主题下各自的解析值：源工程 AndroidManifest 的 android:theme → res/values 与 res/values-night 的 styles.xml / themes.xml；应用没写的，到依赖库包内 res/values*/values*.xml（按应用依赖的版本）和 Android SDK 平台资源 data/res/values/themes*.xml（按 compileSdk）顺着 parent 找；按 Activity 主题 → 应用主题 → 库主题 → 平台主题找第一个写了该属性的 item，再把 @color 引用解析到色值；深色侧没写的取父主题的夜间值
- 应用实际用的 compileSdk 和依赖库版本：源模块构建脚本里的 compileSdk 和 dependencies；到对应版本的平台资源目录和库包里查，不凭记忆
未核实：Activity 主题 → 应用主题 → 库主题 → 平台主题的先后照族里规矩的查法写，没有逐条核对框架源码
来源：3 张卡，3 个应用
- case-0405ee7ad27947343068（2048）：做法第 1 步 ← 建议 2
- case-e1b1f9786e31a8d527cc（AntennaPod）：做法第 1 步 ← 建议 5
- case-e6fd5f0c4d37710c1d97（Blockinger）：做法第 2 步 ← 建议 3
