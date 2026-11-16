# 规格写对话框可见契约时，遮罩写浓度和覆盖范围，显示位置写参照区

审的是：规格
触发（任一种）：
- 读到：安卓源端用 AlertDialog / Dialog 窗口；源主题由应用窗口画状态栏底色（windowDrawsSystemBarBackgrounds、statusBarColor）；全局约定决定「目标保持非全屏」；写错的样子：规格的弹窗契约只写「载体 openCustomDialog 居中卡片」「遮罩 60% 黑」「弹层由宿主窗口避让兜底」「仅做系统栏默认避让」，没写遮罩是否覆盖应用窗口画的状态栏、导航栏底色，没写居中的参照区，也没写目标侧要做的处理
适用范围：规格阶段写对话框的可见契约、并决定目标窗口是否全屏时
做法：
- 遮罩一项写浓度加覆盖范围，例：「遮罩 = 主题 backgroundDimAmount；覆盖应用窗口画的状态栏底色，弹窗期间状态栏压暗、图标不变」
- 显示位置一项写参照区：「对话框在状态栏下沿与导航栏上沿之间居中」
- 在决定「目标保持非全屏」的同一处写明对话框的目标侧处理：弹窗期间切换状态栏底色为压暗色；按顶部与底部避让差的一半下移卡片。「居中卡片」「弹层由宿主窗口避让兜底」不能代替这两项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Material、Theme.Material.Light：windowDrawsSystemBarBackgrounds=true，statusBarColor=?attr/colorPrimaryDark，backgroundDimAmount=0.6：源端状态栏底色由应用窗口画，dim 连状态栏底色一起压暗（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light（按应用的 compileSdk 取对应平台））
- 非全屏窗口的状态栏由系统画在应用窗口之外，openCustomDialog 的遮罩压不到；DialogAlignment.Center 以整窗为基准：目标侧两处差异，契约里要写对应处理（出处：卡里修好并验证过）
针对本应用要查的：
- 源端状态栏底色由谁画、dim 是多少：源工程 AndroidManifest 的 android:theme，到源工程 res/values*/styles.xml 和 Android SDK 平台资源 themes_material.xml 顺着父主题找 windowDrawsSystemBarBackgrounds、statusBarColor、backgroundDimAmount；windowDrawsSystemBarBackgrounds 为 true 且 statusBarColor 不透明时，契约里写「遮罩覆盖应用窗口画的状态栏底色」；dim 照 backgroundDimAmount 写
来源：1 张卡，1 个应用
- case-5056fd5bebd86cb55f92（Sokoban）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2、建议 1；取值 2 ← 诊断
