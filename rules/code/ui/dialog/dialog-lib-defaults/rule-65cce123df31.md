# MaterialDialog 迁成自绘弹窗时，尺寸留白取 material-dialogs 库资源并注资源名

审的是：代码
触发（任一种）：
- 读到：源码只用 MaterialDialog.Builder（material-dialogs）建对话框，项目 res/ 里没有对应的布局；写错的样子：目标自绘弹窗（openCustomDialog / ComponentContent）的头注释写「material 布局语义」这类没有资源出处的数值，自造内边距、字号和 borderRadius，没有按钮栏高度和分隔
适用范围：源端对话框形制来自 material-dialogs 库资源、目标用 ArkUI 自绘弹窗一比一还原时
做法：
- 按应用依赖的版本解包 material-dialogs 的 AAR，逐项抄 res/values/values.xml 的 md_dialog_* dimen 和 layout 里 md_dialog_basic、md_stub_actionbuttons 的几何，写成弹窗常量表
- 常量表里每个数值的注释写出它的资源名（如 md_dialog_* 的 dimen 名），不写无出处的值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按 md_dialog_basic、md_stub_actionbuttons 和 values.xml 的 dimen 重写常量表并加窗口投影：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- material-dialogs 对话框的标题和正文字号与颜色、内容区上下留白、按钮栏高度、圆角：Gradle 缓存 modules-2/files-2.1 下 material-dialogs 的 core-<版本>.aar（或 transforms 下解包后的 res/），按应用依赖的版本取；看 res/values/values.xml 里 md_dialog_ 开头的 dimen、color，和 res/layout/md_dialog_basic.xml、md_stub_actionbuttons.xml；布局里引用的 @dimen/md_… 到 values.xml 读出数值，sp/dp 照搬成 fp/vp；例：0.9.6.0 下标题 20sp、正文 16sp #8a000000、内容上下 8dp、按钮高 48dp、圆角 2dp
未核实：本机 Gradle 缓存里没有 material-dialogs，lookups 里的例子数值出自卡，未照库资源核对
来源：1 张卡，1 个应用
- case-e91d2b9a9a156d1023ec（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
