# 工具栏的高度、标题字号和颜色

agent 会看到什么：源端 Toolbar / ActionBar 的 ?attr/actionBarSize、标题样式和 AppBarLayout 的 ThemeOverlay；产物里自绘工具栏的 .height、.fontSize、.fontWeight 和标题、图标的颜色

## 通用查法

### 源工具栏的高度、标题字号和颜色来自主题时，按提供方和限定目录查出实际值再写

审的是：代码
触发（任一种）：
- 读到：Toolbar 高度是 ?attr/actionBarSize、标题没写 textAppearance，或 AppBarLayout 的 android:theme 指向 ThemeOverlay.*；主题 parent 链到 Theme.AppCompat.* 或 Theme.Material3.* 等；写错的样子：自绘工具栏写成 .height(56)、.fontSize(20)、Color.White 这类凭记忆或照兄弟页抄的字面量
适用范围：源 ActionBar / Toolbar 迁成自绘工具栏，定高度、标题字号字重和颜色时
做法：
- 按「控件 style → 最近祖先的 android:theme → Activity 主题 → 应用主题」找提供值的那一层，沿 parent 定 AppCompat / M2 / M3 代际
- 到依赖库包内 res/values*/ 按主题和组件样式名顺着 @dimen、@macro、?attr 读到 dp、sp 和颜色，values-land 等限定目录各读一遍
- 尺寸写成 base 与 horizontal 下同名的 float 资源引用，颜色写显式值并注明取自哪层主题
针对本应用要查的：
- 提供工具栏取值的那一层主题和它的代际：源工程布局 XML 里 Toolbar 的 style 和祖先 AppBarLayout 的 android:theme、AndroidManifest 的 android:theme，再到 res/values 与 res/values-night 下 styles.xml、themes.xml 的 parent 链；追到 ThemeOverlay.AppCompat.*、Theme.AppCompat.*、Theme.MaterialComponents.* 或 Theme.Material3.* 为止；样式自己覆写了 actionBarSize、android:textColorPrimary、colorControlNormal 的取覆写值
- 该代际在各限定目录下的默认值：应用依赖版本的 androidx.appcompat:appcompat、com.google.android.material:material 包内 res/values*/ 下的 values*.xml，按 actionBarSize、abc_action_bar_default_height_material、titleTextAppearance、m3_comp_top_app_bar_small_container_height 等名字找；顺着引用读到具体值。例：appcompat 1.7.0 的 abc_action_bar_default_height_material 竖屏 56dp、values-land 48dp；material 1.12.0 的 Material3 主题下 actionBarSize 解析到 64dp
来源：3 张卡，2 个应用
- case-6d63b644ee5d30db83f4（Privacy Friendly 2048）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-a3dc4d0187d7ddc456e8（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-46b47b9e6102｜?attr/actionBarSize 等主题取值先沿 parent 链定 Material 代际再取默认值｜读到：MaterialToolbar 的 android:layout_height="?attr/actionBarSize"、BottomNavigationView，布局不写具体数值；styles.xml 里主题 parent=Theme.Material3.* 或 Theme.MaterialComponents.*；写错：代码或 float 资源写成 56（「Material 默认 56dp」），理由只是 grep 不到 actionBarSize 的显式覆写
- rule-b684467f5d28｜源主题是 Material3 时，自绘工具栏高 64、标题 22 号 Normal、标题起点 16｜读到：styles.xml 的主题 parent 链到 Theme.Material3.*，toolbarStyle parent=Widget.Material3.Toolbar，布局用 MaterialToolbar；写错：自绘工具栏写成 Row 高 56、标题 .fontSize(20).fontWeight(FontWeight.Medium)、.margin({ left: 16 }) 加 Row padding 12 这类 AppCompat / M2 默认
- rule-8c8a5c20b402｜标题栏高度写 ?attr/actionBarSize 时，目标引用分方向的资源键，不写 56 / 20 字面量｜读到：源布局 Toolbar 的 android:layout_height="?attr/actionBarSize"，标题没写 textAppearance / textSize，主题继承 Theme.AppCompat.*（窗口 ActionBar 或 Toolbar），Activity 没锁定方向；写错：目标标题栏写成 `const …: number = 56` 常量、.height(56)、标题 .fontSize(20) 这类不随方向变化的字面量
- rule-ca77660fcef6｜AppBarLayout 带 ThemeOverlay 时，工具栏标题和图标按覆盖取色，不按 DarkActionBar｜读到：AppBarLayout / Toolbar 的 android:theme 的 parent 是 ThemeOverlay.AppCompat.Light，没写 titleTextColor，Activity 主题 *.DarkActionBar；写错：标题 fontColor 和汉堡图标写成白色（Color.White 或 #FFFFFF），注释称按 DarkActionBar「推断」
- rule-9e5ad434b696｜自绘栏复刻框架 ActionBar 时，按 elevation 加 shadow，宿主用 zIndex 压在内容上｜读到：源端用窗口 ActionBar（生效主题的 actionBarStyle 属 Widget.Material.ActionBar 一族），布局里看不到它的 elevation；写错：复刻 ActionBar 的共享标题栏 Row 只有 .backgroundColor(...)，没有 .shadow(...)；宿主页面放它时没有 .zIndex(...)，投影被下面的内容盖住
- rule-88aa2bca4aa5｜取框架 ActionBar 默认外观时，每个平台资源名都查 values-land、values-sw* 覆盖并写成分支｜读到：源 Activity 依赖框架主题自带的 ActionBar，栏高、标题字号等外观取自平台资源，源端没有自己定义；写错：目标自绘标题栏只给一项做方向分支（如栏高 isLandscape ? 48 : 56），标题仍写死 .fontSize(20)
- rule-b475d42173ab｜标题栏 Up 区按 Material 的 Toolbar 导航钮样式取宽和标题起点，不凑近似值｜读到：源主题是 Theme.Material 系的窗口 ActionBar，页面 setDisplayHomeAsUpEnabled(true)；写错：Up 区写成 minWidth 加对称 padding、标题左距凑数并注「近似」
- rule-fe06f7b6fbfd｜标题栏溢出钮按 Material 溢出钮样式分侧取内距，不按最小宽对称近似｜读到：源主题是 Theme.Material 系的窗口 ActionBar，菜单有进溢出的项；写错：溢出钮按 action_button_min_width_overflow_material 对称取左右 padding
