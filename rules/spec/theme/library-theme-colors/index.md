# AppCompat / MaterialComponents 主题的语义色

agent 会看到什么：读到 styles.xml / themes.xml 里应用主题继承 Theme.AppCompat.DayNight 或 Theme.MaterialComponents.*，控件没写颜色、颜色来自 colorPrimary 等主题属性，values-night 里可能有同名主题；规格写「零硬编码色值」「沿用 base」「DayNight → resources/dark」，没有主题色的浅深两态值

## 通用查法

### 主题色来自 AppCompat / MaterialComponents 库主题时，规格写出库里解析出的浅深两态值

审的是：规格
触发（任一种）：
- 读到：源控件没写颜色属性，或颜色写成 colorPrimary / colorAccent 等主题属性；应用主题的 parent 链到 Theme.AppCompat.* 或 Theme.MaterialComponents.*；写错的样子：规格写「颜色由资源系统负责」「沿用 base / 日间值」「框架默认色不猜」，没有主题色的浅深两态值和 $r('app.color.…') 键
适用范围：源端颜色由 AppCompat / MaterialComponents 库主题提供，规格写主题、颜色和控件外观时
做法：
- 从控件的 style（没写取主题的默认样式）和应用主题出发沿 parent 链找这一项：应用写了的先用，没写的到依赖库找；夜间先看 values-night 的同名主题，没写的项取父主题夜间那一支
- 找到的 item 顺着 @color/、?attr/、@android:color/ 解析到十六进制值，浅深各一份
- 规格在用到它的那一行写出值和成对的 base / dark 颜色键，页面写 $r('app.color.<键>')
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.AppCompat.DayNight：values 下 parent="Theme.AppCompat.Light"，values-night-v8 下 parent="Theme.AppCompat"：DayNight 的浅色到 Light 那一支取值，深色到 Theme.AppCompat 那一支取值（出处：androidx.appcompat:appcompat 包内 res/values/values.xml 与 res/values-night-v8/values-night-v8.xml，Theme.AppCompat.DayNight（按应用依赖的版本））
针对本应用要查的：
- 应用主题的 parent 链和应用自己写了的主题色项：源工程 res/values/ 与 res/values-night/ 下的 styles.xml、themes.xml，按 AndroidManifest 里 android:theme 的主题名找同名 style；逐级记下 parent 和写了的 item；夜间块里没写的项记为要到父主题夜间那一支取
- 依赖库主题对这一项的默认值：应用依赖版本的 androidx.appcompat:appcompat 或 com.google.android.material:material 包内 res/values/values.xml（夜间看 values-night 一类目录），按 style 名顺着 parent 找 item；顺着 @color/、?attr/、@android:color/ 解析到十六进制值；例：appcompat 1.7.1 下 Theme.AppCompat 的 colorPrimary 是 @color/primary_material_dark，解析为 #ff212121
未核实：MaterialComponents 主题各项颜色的夜间默认值，本族规矩没有逐项查过；values-night-v8 是 appcompat 1.7.1 的夜间目录名，其他版本没核对
来源：3 张卡，3 个应用
- case-7af8ba0d85382021da91（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-97a40a9d2dce65dc9f9c（Dice Roller）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-07b9e7096fae｜源 Button 没写样式、主题是 MaterialComponents 系时，规格按钮行写明底色字色圆角最小高度｜读到：源布局里 Button 没写 android:background、backgroundTint、textColor、cornerRadius，应用主题的父主题是 Theme.MaterialComponents.*，设计令牌里有 colorPrimary、colorOnPrimary；写错：规格里这个 Button 的转换决策行只有文案、字号、边距；主题色只在全局写一句“颜色由资源系统负责”或“页面代码零硬编码色值”，按钮行没有底色、字色、圆角
- rule-2d58cbc798c9｜规格写“页面零硬编码色值”时，同句写明要用 $r('app.color.…') 引用语义色｜读到：源端颜色来自主题语义色（colorPrimary、colorOnPrimary 等），深浅色分 values / values-night 两套；写错：规格或功能规格写“页面代码零硬编码色值”“主题深浅色 out of scope”，没写允许并要求用 $r('app.color.…') 引用已迁移的语义色
- rule-591815630884｜AppTheme 只继承 Theme.AppCompat.DayNight 时，规格列出框架色浅深取值作成对 token｜读到：styles.xml 里 AppTheme 只有 parent="Theme.AppCompat.DayNight"，没有 colorPrimary / colorAccent 覆写，资源目录没有 values-night；写错：跨栈映射写成「DayNight 主题 → resources/dark（业务色双目录）| colors.xml 转 color.json」，没列框架主题浅/深两态的窗口、ActionBar、按钮、文字、强调色等取值
- rule-a7c903aab652｜values-night 重定义同名主题却没写日间的主题色项时，规格写出父主题的夜间默认值｜读到：values-night/styles.xml 里有与日间同名的 AppTheme（parent 是 Theme.AppCompat.DayNight 一族），日间写过的 colorPrimary / colorPrimaryDark / colorAccent 在夜间块里没写；写错：规格、页面规格或决策台账写「夜间仅覆盖某几项」「其余沿用 base / 日间值」，或写「框架默认色不猜」，没写这几项主题属性的夜间值，也没登记未决
