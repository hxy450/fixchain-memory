# 主题、平台或库提供的颜色和外观值

agent 会看到什么：源端颜色或外观不是自己写的值，而来自主题属性（?attr、?android:attr）、控件默认（没写 android:textColor）、平台 @android: 资源或依赖库主题（AppCompat、Material3、Holo、GlanceTheme）；color.json 等里是凭记忆的近似值、模板值，base 和 dark 同值或缺 dark 键

## 通用查法

### 颜色来自主题或平台、库默认时，浅深主题分别沿 parent 链解析，base 和 dark 各写

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

## 规矩

- rule-1116995d4cea｜为 ?attr/xxx 新建颜色键时分别查各主题的值，base 和 dark 各写各的｜读到：源布局 android:textColor="?attr/colorOnSecondary" 这类引用主题属性的颜色，styles.xml 里浅色、深色主题各有一块；写错：resources/base/element/color.json 和 resources/dark/element/color.json 里这个颜色键写了同一个值（凭「accent 底上偏白」推断）
- rule-a5d05951a3c1｜布局用 ?attr 引用主题色时，给每个主题属性建 base/dark 成对颜色键，@color 写死的保留单态｜读到：布局里有 ?attr/colorPrimary、?attr/colorAccent（Toolbar、ActionBar、抽屉选中项），主题里设了这些属性且日夜取值不同；另有 @color/colorPrimary 写死的引用；写错：base/element/color.json 里只有 colors.xml 直迁的 colorPrimary 等单态常量，dark/element/color.json 里没有主题属性对应的同名键
- rule-f1a09810d4b5｜Text 要用主题次要文字色而目标工程没有这项颜色资源时，base 和 dark 各补一份｜读到：源 TextView 没写 android:textColor，颜色来自 DayNight 一类主题的 ?android:textColorSecondary；写错：resources/base/element/color.json 里没有对应的次要文字色；或者只在 base 里有，resources/dark/element/color.json 缺同名项
- rule-995bbdd589d4｜给源端默认字色建的颜色键，base 和 dark 照 TextView 默认链取次级文字色，不填主文字色｜读到：源 TextView 没写 android:textColor，主题继承 Theme.AppCompat.DayNight.* 或平台 Material 主题，且未覆盖 textAppearanceSmall、textColorTertiary；写错：目标 base/element/color.json 为这些文字新建的键填 #DE000000，dark/element/color.json 填 #FFFFFFFF（主文字色的取值）
- rule-abef27bb444c｜建主题文字色令牌前先查 SDK，不把近似值或旧注释里的「平台默认」写进共享 color.json｜读到：源 styles 父链止于 android:Theme.Holo 等平台主题，文字色由平台提供；写错：resources/base/element/color.json 里新建的主题文字色令牌是半透明白（#B3FFFFFF、#80FFFFFF）、纯白或记忆中的灰值，「待核」只写在报告里
- rule-101e8cac387c｜框架默认色写进共享 color.json 时，base/dark 成对写，取值按依赖版本资源核对｜读到：styles.xml 里 AppTheme 只继承 Theme.AppCompat.DayNight，没有 values-night；写错：dark/element/color.json 只是 base 业务色的镜像（注释「无 values-night，镜像 base」）；框架色键只在 base 有、dark 没有，或写的是凭记忆的框架默认值（如 color_accent）
- rule-6065396fba3a｜启动窗底色取源主题的背景色，Light 主题无 values-night 时 dark 也写同一浅色｜读到：源主题继承 Theme.AppCompat.Light 等 Light 系主题、没有 values-night，主题里没写 android:windowSplashScreenBackground；写错：start_window_background 在 base/element/color.json 保留脚手架 #FFFFFF、dark/element/color.json 保留 #000000，资源映射里记为「模板保留」
- rule-0f07b03a1e21｜M3 主题的对话框遮罩色资源按 0.32 黑写成 #52000000，不用平台旧默认 0.6 的 #99000000｜读到：styles.xml 的应用主题沿 parent 链继承 `Theme.Material3.*`，主题里有 `android:backgroundDimEnabled`=true；写错：base 或 dark 的 color.json 里新增的遮罩色是 `#99000000`（按平台默认 backgroundDimAmount 0.6 推出）
- rule-b52b998d19db｜tint 用随深浅主题变的颜色做渐变时，base 和 dark 各写一份主题色和它的透明变体｜读到：ImageView 的 app:tint 引用 ?android:attr/colorBackground 这类随主题变的颜色，给白到透明的渐变 shape 着色；写错：目标 resources/base/element/color.json 只有主题色没有对应的透明变体，或 resources/dark/element/color.json 里缺这两项
- rule-2e1f039111c0｜图标或控件引用主题属性时，color.json 在 base 和 dark 各写一个键，值取主题解析值｜读到：源图标或控件着色引用主题属性：矢量 android:fillColor="?attr/…"、app:foregroundColor="?attr/…"、Toolbar 主题的 colorControlNormal；写错：resources/base/element/color.json 里没有对应的键，或者只有 base 值、resources/dark/element/color.json 里没有深色值
- rule-557317f85a4f｜落 @android:color 和 ?android:attr 的值时，从本机 SDK 平台资源取实值并注明来源｜读到：源 XML 引用 @android:color/darker_gray、?android:attr/expandableListPreferredItemPaddingLeft 这类平台值；写错：color.json / float.json 里写的是凭记忆的值（如 darker_gray 写成 #FF444444、缩进写成 60vp），或报告写「依据为 AOSP attr 默认值，待真机校对」
- rule-31569360600c｜平台主题提供的 ActionBar 外观，从本机 Android SDK 平台资源取值和原图，不凭记忆近似｜读到：主题 parent 链止于 android:Theme.Holo，ActionBar 是主题提供的窗口装饰、不在布局 XML 里；写错：color.json 里写凭记忆的近似底色（如 #FF333333，注「待核」）；media 里没有 Up 尖角和溢出按钮的原图
- rule-89ea380b6cb1｜GlanceTheme 的颜色迁成 color.json 时，取 Glance 库的回退色，不用 M3 基线近似｜读到：源端用 GlanceTheme.colors.widgetBackground（或 GlanceTheme 的其他颜色角色）作背景或前景；写错：base 或 dark 的 color.json 里写的是 Material 3 baseline 色（如 #FEF7FF、深色 #1C1B1F）或注明「近似」
- rule-79c01fd67265｜源端依赖 appcompat 或 material 时，把库限定目录的尺寸导出到 base 和 horizontal｜读到：模块构建脚本声明 androidx.appcompat:appcompat / com.google.android.material:material，布局或主题引用 ?attr/actionBarSize 等库主题属性；应用自己的 res 里没有 values-land 覆盖；写错：只在 resources/base/element/float.json 写标题栏高度、字号的单值，没有 resources/horizontal/element/float.json 覆盖；资源映射表写「零外部资源依赖库」
- rule-8848f86636bb｜@android:color 系统色按固定表转十六进制，动态色无引用就删、有引用给明确 hex 回退｜读到：colors.xml 的值引用 @android:color/black、@android:color/white、@android:color/transparent，或 Android 12+ 动态色 @android:color/system_accent1_500、system_neutral1_*、system_error_* 一类；写错：color.json 里原样写着 @android:color/…，或动态色条目既没有 hex 回退、映射文档也没注明近似
- rule-db162ee1b392｜复刻 NavigationView 默认外观时，在 color.json 登记选中底色、未选图标色和分隔线色｜读到：NavigationView 没写 itemIconTint、itemBackground，菜单项外观来自 Material 默认样式；写错：目标 element/color.json 没有菜单项选中底色、未选图标着色、分隔线色的键，抽屉只复用已有的主色、black 和近名灰
