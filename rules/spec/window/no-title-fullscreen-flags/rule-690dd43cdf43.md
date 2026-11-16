# 源 Activity 带去标题或全屏标志时，规格按标志查清隐藏的是哪一栏，逐边写系统栏形态

审的是：规格
触发（任一种）：
- 读到：源 Activity 调 requestWindowFeature(FEATURE_NO_TITLE)、setFlags(FLAG_FULLSCREEN)，或主题是 Theme.*.NoTitleBar[.Fullscreen]、带 windowNoTitle / windowFullscreen；写错的样子：规格写「无标题全屏」「真全屏」「沉浸式」，没逐边写标题栏、状态栏、导航栏哪个隐藏
适用范围：规格提取阶段解读源端窗口标志、写目标系统栏和安全区时
做法：
- 收齐页面生效的标志：代码里的 requestWindowFeature / setFlags，加上 Manifest 给它的主题及父主题里的 windowNoTitle、windowFullscreen
- 逐个标志查它隐藏哪一栏：FEATURE_NO_TITLE / windowNoTitle 只去标题栏；FLAG_FULLSCREEN / windowFullscreen 只隐藏状态栏，不涉及导航栏
- 规格逐边写：三栏各自隐藏还是保留，应用窗口止于哪里，背景和内容向哪边延伸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FEATURE_NO_TITLE：Flag for the "no title" feature, turning off the title at the top of the screen：只关标题，不涉及状态栏（出处：android.view.Window#FEATURE_NO_TITLE）
- windowNoTitle：Flag indicating whether there should be no title on this window；windowFullscreen 是另一项：去标题和全屏是两个独立的主题属性（出处：Android SDK 平台资源 data/res/values/attrs.xml，Window 的 windowNoTitle、windowFullscreen（按应用的 compileSdk 取对应平台））
- FLAG_FULLSCREEN：窗口在顶层时隐藏状态栏；主题里的 android:windowFullscreen 控制同一个旗标：代码旗标和主题属性同义，只对应状态栏（出处：android.view.WindowManager.LayoutParams#FLAG_FULLSCREEN）
- 参照机上 FLAG_FULLSCREEN 窗口：状态栏隐藏、导航栏保留、应用窗口止于导航栏之上：例：只有 FLAG_FULLSCREEN 时源端的实际形态（出处：卡里修好并验证过）
针对本应用要查的：
- 这个页面实际生效的窗口标志：源工程 AndroidManifest.xml 里这个 Activity 的 android:theme（没有就看 application 的），再到 res/values 的样式文件里顺着 parent 找；Activity 的 onCreate 里 setContentView 之前的 requestWindowFeature / getWindow().setFlags；读出 windowNoTitle、windowFullscreen 的取值和代码里设的标志，合起来定标题栏和状态栏是否隐藏
未核实：父主题里的 windowNoTitle / windowFullscreen 怎么被子主题覆盖、各平台主题分别设了哪些，族里规矩没有查过平台的主题文件；隐藏导航栏或延伸到系统栏下的其他标志，族里规矩没有查过
来源：2 张卡，2 个应用
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-bbb49cc9ec510f04eb33（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 4 ← 诊断
