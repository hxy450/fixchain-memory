# 框架默认色写进共享 color.json 时，base/dark 成对写，取值按依赖版本资源核对

审的是：资源
触发（任一种）：
- 读到：styles.xml 里 AppTheme 只继承 Theme.AppCompat.DayNight，没有 values-night；写错的样子：dark/element/color.json 只是 base 业务色的镜像（注释「无 values-night，镜像 base」）；框架色键只在 base 有、dark 没有，或写的是凭记忆的框架默认值（如 color_accent）
适用范围：源工程是未覆写的 AppCompat DayNight，写目标端共享 color.json 时
做法：
- 框架色在 base/element/color.json 和 dark/element/color.json 成对写同名键（窗口、ActionBar、状态栏、按钮常态/按下、对话框、次级/提示/禁用文字、分隔线、进度轨道）
- 取值按应用依赖的 appcompat 版本资源或源端运行截图核对后再写；核不了的登记未决，不在共享资源里落猜测值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在 base/element/color.json 和 dark/element/color.json 里定义同名配色并赋予不同色值：跟随系统深浅色的颜色资源写法（出处：ui-dark-light-color-adaptation.md，应用跟随系统的深浅色模式）
- 例：appcompat 1.7.1 下浅色 colorAccent 解析为 material_deep_teal_500 = #ff008577：凭记忆写的值可能和依赖版本不同（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，material_deep_teal_500（按应用依赖的版本））
针对本应用要查的：
- 每个框架色键的浅/深取值：androidx.appcompat:appcompat 包内 res/values/values.xml（浅色）和 res/values-night-v8/values-night-v8.xml（深色）；从 Base.V7.Theme.AppCompat.Light / Base.V7.Theme.AppCompat 的 item 顺着 @color/… 引用解析到色值；拿不到时用源端运行截图取色
来源：1 张卡，1 个应用
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 2
