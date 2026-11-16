# 对话框库 Builder 建的对话框（material-dialogs）的形制和排版缺省

agent 会看到什么：读到源端用 material-dialogs 等对话框库的 MaterialDialog.Builder（customView、positiveText）建对话框，项目 res/ 里没有对应布局，库内的 dimen、布局几何和 Builder 缺省（如正文 setLineSpacing）不在源码树里；产物里自绘弹窗的内边距、字号、圆角、按钮栏高度和正文 lineSpacing 有没有出处

## 通用查法

### 源端对话框出自第三方库 Builder 时，按依赖版本读库资源和 Builder 缺省，写成带出处的常量

审的是：代码
触发（任一种）：
- 读到：源端用 material-dialogs 等对话框库的 Builder（MaterialDialog.Builder(…)…show()）建对话框，项目 res/ 里没有对应的布局和 dimen；写错的样子：目标自绘弹窗（openCustomDialog / ComponentContent / @CustomDialog）的 padding、fontSize、borderRadius、lineSpacing 是没有资源出处的数值，或者只复刻了内边距和字号
适用范围：源端对话框的形制和排版缺省来自第三方对话框库、目标用 ArkUI 自绘弹窗还原时
做法：
- 按应用依赖的库版本取库包：形制看 AAR 的 res/values/values.xml（库前缀的 dimen、color）和 res/layout 里对话框布局的几何；排版缺省看库源码里对话框 Builder 的字段初值和初始化正文的那段
- 把读出的值写成弹窗常量，注释写出资源名或 Builder 字段名；sp、dp 照搬成 fp、vp，行距倍数一类换算成目标端对应属性（如正文 Text 的 .lineSpacing）
针对本应用要查的：
- 库的依赖版本：源工程模块的 Gradle 构建脚本里这个库的依赖坐标；读出版本号，按这个版本去 Gradle 缓存里找库包和源码
- 对话框的字号、颜色、内容区留白、按钮栏高度、圆角：Gradle 缓存 modules-2/files-2.1 下这个库同版本的 AAR（或 transforms 下解包后的 res/），看 res/values/values.xml 里库前缀（如 md_dialog_）的 dimen、color 和 res/layout 里的对话框布局；布局里引用的 @dimen/… 到 values.xml 读出数值；例：卡里 material-dialogs 0.9.6.0 下标题 20sp、正文 16sp、内容上下 8dp、按钮高 48dp、圆角 2dp
- Builder 的正文排版缺省：同版本库源码里对话框 Builder 的字段初值和初始化正文的代码（如 content.setLineSpacing(…)）；读出行距倍数、额外行距等，写进组件注释并换算成目标属性；例：卡里的库缺省 contentLineSpacingMultiplier 是 1.2
未核实：本机 Gradle 缓存里没有 material-dialogs，例子里的数值出自卡，没有照库资源核对
来源：2 张卡，1 个应用
- case-a767fbce6dbdeb152c90（omni-notes-hmos）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
- case-e91d2b9a9a156d1023ec（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-65cce123df31｜MaterialDialog 迁成自绘弹窗时，尺寸留白取 material-dialogs 库资源并注资源名｜读到：源码只用 MaterialDialog.Builder（material-dialogs）建对话框，项目 res/ 里没有对应的布局；写错：目标自绘弹窗（openCustomDialog / ComponentContent）的头注释写「material 布局语义」这类没有资源出处的数值，自造内边距、字号和 borderRadius，没有按钮栏高度和分隔
- rule-e4757fd0dc9e｜以对话框库为锚点封装对话框时，把库 Builder 的行距倍数缺省落成正文 lineSpacing｜读到：源端用 material-dialogs 等对话框库的 Builder 构造对话框（库内对正文 setLineSpacing(0, 1.2) 这类缺省不在源码树里）；写错：目标对话框正文 Text 只有 fontSize / fontColor，没有 .lineSpacing(…)，注释却声称对齐库的布局语义
