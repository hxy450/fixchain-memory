# FEATURE_NO_TITLE、NoTitleBar 只去标题栏，规格不写成「全屏语义」

审的是：规格
触发（任一种）：
- 读到：Activity 只调用 requestWindowFeature(Window.FEATURE_NO_TITLE)，或主题是 Theme.*.NoTitleBar，没有 windowFullscreen / FLAG_FULLSCREEN；写错的样子：规格写「FEATURE_NO_TITLE 全屏语义照搬」「无标题全屏」，顶部不避让、内容从屏顶画起
适用范围：规格阶段解读源端去标题栏写法、决定页面是否全屏时
做法：
- 规格把 FEATURE_NO_TITLE / NoTitleBar 写成「去掉标题栏或 ActionBar，状态栏照常显示」；只有 windowFullscreen 或 FLAG_FULLSCREEN 才写隐藏状态栏
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FEATURE_NO_TITLE：Flag for the "no title" feature, turning off the title at the top of the screen：只关标题，不涉及状态栏（出处：android.view.Window#FEATURE_NO_TITLE）
- windowNoTitle：Flag indicating whether there should be no title on this window；windowFullscreen 是另一项：去标题和全屏是两个独立的主题属性（出处：Android SDK 平台资源 data/res/values/attrs.xml，Window 的 windowNoTitle、windowFullscreen（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 2
