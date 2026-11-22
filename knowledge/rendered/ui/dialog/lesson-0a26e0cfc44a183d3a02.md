# 用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，按钮行先按源取值定高再让分隔线撑满（平台 AlertDialog 的按钮条取平台样式或实测，不默认 48vp）

## 何时使用

界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级与卡片、按钮行的高度约束时

## 适用情境

源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，布局是固定宽、wrap_content 高的卡片，按钮行内有 layout_height=match_parent 的竖分隔 View；触发按钮位于 Tabs 子页或嵌套组件内。 也包括按钮由 AlertDialog.Builder 的 setPositive/Negative/NeutralButton 生成、源布局里没有按钮行，按钮条外观来自主题的平台对话框样式。

## 例外与边界

- 改用 openCustomDialog、bindSheet 等系统弹窗 API 时，遮罩由框架负责（openCustomDialog 默认挂在应用窗口根节点、蒙层盖整窗；levelMode 设为 EMBEDDED 时挂在页面内、蒙层按父节点约束显示；isModal 为 false 或 bindSheet 为跟手样式时默认无蒙层），按真弹窗写法处理

## 原因

覆层挂在触发按钮所在的 Tab 子组件里，遮罩只盖到该子组件区域，底部 Tab 栏仍亮、仍可点；按钮行不定高而只给分隔线 Stretch 时，Stretch 子项会把行和卡片撑到父容器全高。来源中写者已读到 Dialog 由 Activity 创建、Theme.Dialog 浮动窗口、卡片 wrap_content 与按钮行实测高度，宿主根 Stack 上也已挂过同类弹窗，仍把覆层写进 Tab 内；真机 dump 显示卡片撑成全高、dim 未盖住 Tab 栏，随后才改为宿主根挂载并给按钮行定高。平台对话框的按钮条高度不在应用源码里；经验摘要里的“按钮行先定高（48vp）”会被直接当作取值。

## 做法

1. 源弹窗属于 Activity 窗口时，覆层挂在覆盖整个窗口的宿主根容器（如主页根 Stack），不挂在触发按钮所在的子组件；子组件通过共享状态或回调请求宿主显示和关闭，返回键拦截也放在宿主。
2. 转换按钮行里 match_parent 高的分隔 View 时，先给所在 Row 确定高度：应用布局里的按钮取源按钮实测或由 padding 与字号计算；平台 AlertDialog 的按钮条取平台样式或源端实测（如 Holo 按钮条实测约 53.33dp，上方另有分隔线；平台样式只给按钮最小高 alert_dialog_button_bar_height：48dip，可用屏高 ≥720dp 时 54dip，Material 与 AppCompat 按钮条另有上下各 4dp 内边距），取不到标待核，不默认 48vp。再让分隔线 Stretch 或取 100%；不让未定高 Row 中的 Stretch 子项决定卡片高度。

## 可选检查

- 覆层写完用真机 dump 核两组 bounds：卡片高度接近源端实测，遮罩覆盖源 dim 覆盖的整个窗口（含底部 Tab 栏）。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕android.app.Dialog 构造时用传入的 Context 取得呈现对话框的 WindowManager 和基础主题：用 Activity 创建的 Dialog 是由该 Activity 的 WindowManager 添加的独立窗口，不在任何 Fragment 的视图树里
- 〔适用情境 / 做法第 1 步〕应用没有另设对话框主题时，平台 Theme.Dialog 设 windowIsFloating=true，基础主题 Theme 的 backgroundDimAmount 为 0.6：对话框是浮动窗口，背后整个窗口按 0.6 变暗
- 〔做法第 1 步〕自定义组件的 onBackPress 只对 @Entry 装饰的组件生效；返回 true 表示页面自己处理返回，返回 false（默认）走默认返回逻辑
- 〔原因 / 做法第 1 步〕条件渲染的全幅遮罩加卡片挂在 Tabs 子页组件内时，真机上遮罩只覆盖该子组件的区域，底部 Tab 栏不被遮住、仍可点击
- 〔原因 / 做法第 2 步〕ItemAlign.Stretch：除设了 FlexWrap.Wrap / WrapReverse 的 Flex 外，元素无论是否设了尺寸，都沿交叉轴拉伸到容器尺寸
- 〔原因 / 做法第 2 步〕按钮 Row 没有确定高度、其中的竖分隔线按 Stretch 拉伸时，真机上 Row 和外层卡片被撑到父容器的全高
- 〔做法第 2 步〕平台 Material 警告框按钮样式 Widget.Material.Button.ButtonBar.AlertDialog 的 minHeight 取 alert_dialog_button_bar_height：values 下 48dip，values-h720dp（可用屏高 ≥720dp）下 54dip；这只是按钮最小高，不是按钮条总高
- 〔做法第 2 步〕平台 Material 警告框的按钮条布局 alert_dialog_button_bar_material 里 ButtonBarLayout 设 paddingTop、paddingBottom 各 4dp，paddingStart、paddingEnd 各 12dp
