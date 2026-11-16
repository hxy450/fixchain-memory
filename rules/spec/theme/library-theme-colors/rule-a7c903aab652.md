# values-night 重定义同名主题却没写日间的主题色项时，规格写出父主题的夜间默认值

审的是：规格
触发（任一种）：
- 读到：values-night/styles.xml 里有与日间同名的 AppTheme（parent 是 Theme.AppCompat.DayNight 一族），日间写过的 colorPrimary / colorPrimaryDark / colorAccent 在夜间块里没写；写错的样子：规格、页面规格或决策台账写「夜间仅覆盖某几项」「其余沿用 base / 日间值」，或写「框架默认色不猜」，没写这几项主题属性的夜间值，也没登记未决
适用范围：源主题继承 Theme.AppCompat.DayNight 一族、values-night 重定义了同名主题，提取深浅色差分时
做法：
- 读 values-night 等限定目录的 styles 全文，不按 overlay 名 grep；对同名 style 逐项比日间：夜间块里没写的项取父主题的夜间默认，不沿用日间值
- 规格里逐项写出夜间值，如「colorPrimary 夜间 = AppCompat 深色默认 #212121」；默认值查不到时登记未决，不以「不猜」为由不写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 夜间 Theme.AppCompat.DayNight 和 Theme.AppCompat.DayNight.DarkActionBar 的 parent 都是 Theme.AppCompat：夜间没写的项回落到深色的 Theme.AppCompat（出处：androidx.appcompat:appcompat 包内 res/values-night-v8/values-night-v8.xml，Theme.AppCompat.DayNight、Theme.AppCompat.DayNight.DarkActionBar（按应用依赖的版本））
- Base.V7.Theme.AppCompat：colorPrimary=@color/primary_material_dark，colorPrimaryDark=@color/primary_dark_material_dark，colorAccent=@color/accent_material_dark：Theme.AppCompat 经 Base.Theme.AppCompat 继承到的三项默认（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Theme.AppCompat（按应用依赖的版本））
- primary_material_dark=@color/material_grey_900=#ff212121；primary_dark_material_dark=@android:color/black=#ff000000；accent_material_dark=@color/material_deep_teal_200=#ff80cbc4：三项默认解析到的十六进制值（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，primary_material_dark、primary_dark_material_dark、accent_material_dark（按应用依赖的版本）；Android SDK 平台资源 data/res/values/colors.xml，black）
- 夜间回落后，用 ?attr 引用的工具栏、ActionBar、状态栏区和强调色跟着变，@color/ 写死的不变：哪些位置受夜间回落影响（出处：卡里修好并验证过）
针对本应用要查的：
- 应用依赖的 appcompat 版本下父主题的夜间默认：依赖库 androidx.appcompat:appcompat（按应用依赖的版本）包内 res/values-night-v8/values-night-v8.xml 找父主题夜间的 parent，再到 res/values/values.xml 顺着 parent 链找 colorPrimary 等 item；顺着 @color、@android:color 引用解析到十六进制值；例：1.7.1 下 colorPrimary 夜间是 #ff212121
未核实：卡里没记 appcompat 版本，默认值按本机缓存的 appcompat 1.7.1 核实
来源：1 张卡，1 个应用
- case-7af8ba0d85382021da91（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2；取值 4 ← 诊断
