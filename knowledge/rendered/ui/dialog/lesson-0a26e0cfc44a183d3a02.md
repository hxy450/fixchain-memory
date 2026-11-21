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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；实现对照 OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release；安卓 Android SDK 平台资源 android-30、android-36、android-37.0；Android SDK 源码 android-36.1；appcompat 1.1.0、1.8.0；material 1.14.0（只核主题覆盖名）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕平台 android.app.AlertDialog 在 Material 主题下的按钮条是 ButtonBarLayout，上下内边距各 4dp、左右各 12dp，按钮最小高取 alert_dialog_button_bar_height；在 Holo 主题下按钮条外层 buttonPanel 与三个按钮的最小高都取 alert_dialog_button_bar_height，上方有一条 dividerHorizontal 分隔线，没有上下内边距。alert_dialog_button_bar_height 默认 48dip，可用屏幕高度 ≥720dp（资源限定符 h720dp）时为 54dip。〔成立范围：对 Theme.Material、Theme.Material.Light 与 Theme.Holo 系对话框主题成立（AlertDialog.Material 的布局为 alert_dialog_material，Holo 为 alert_dialog_holo），android-30、36、37.0 资源一致；h720dp 按当前方向的可用高度判断，同一设备横竖屏可能不同；按钮文字换行时按钮更高（Holo 按钮 maxLines 为 2）；Material 的 ButtonBarLayout 默认允许叠放，按钮横排放不下时改为竖排，按钮条随之变高。不成立：电视（values-television 改用 Leanback 对话框主题）、手表（values-watch 中该高度为 0dp）、由厂商改过的 Theme.DeviceDefault 系列，以及 AppCompat 与 MaterialAlertDialogBuilder（见另条）。〕
- 〔做法第 2 步〕androidx.appcompat 的 AlertDialog 按钮条（abc_alert_dialog_button_bar_material）是 ButtonBarLayout，上下内边距各 4dp、左右各 12dp；按钮样式 Widget.AppCompat.Button.ButtonBar.AlertDialog 的最小高为 abc_alert_dialog_button_bar_height（默认 48dp，h720dp 时 54dip），最小宽 64dp。〔成立范围：appcompat 1.1.0 与 1.8.0 相同；对 androidx.appcompat.app.AlertDialog 配 Theme.AppCompat 系对话框主题成立；ButtonBarLayout 的 allowStacking 默认为 true，按钮横排放不下时改为竖排，按钮条随之变高。不成立：用 com.google.android.material 的 MaterialAlertDialogBuilder 时会套主题的 materialAlertDialogTheme（MaterialComponents 主题下为 ThemeOverlay.MaterialComponents.MaterialAlertDialog，Material3 主题下为 ThemeOverlay.Material3.MaterialAlertDialog），按钮样式改为 TextButton.Dialog 一类，不按此值；应用主题覆写了 buttonBarPositiveButtonStyle 等属性时随覆写。〕
- 〔做法第 1 步〕TabContent 不设 clip 时默认 clip 为 true，Tabs 同样默认裁剪；写在 TabContent 内容里的覆层即使用 position、负 offset 或很大的 zIndex，也画不到、点不到 TabContent 范围之外（含 TabBar）；zIndex 只调整同一父节点内兄弟的堆叠顺序，不能把节点提到别的容器之上。〔成立范围：依据是 TabContent 文档的说明、clip 文档（设为 true 后超出部分不响应手势）、background 文档的默认裁剪组件清单（含 Tabs、Swiper、List、Scroll 等）与 zIndex 文档；命中部分的实现见 OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release 的 FrameNode::IsOutOfTouchTestRegion。TabContent 关掉 clip 后仍受外层 Tabs 默认裁剪限制。不成立：用 openCustomDialog 等挂到应用窗口根节点的弹窗（levelMode 为 OVERLAY）时不受页面内容器裁剪。〕
- 〔例外与边界〕promptAction.openCustomDialog 未另设时 levelMode 为 LevelMode.OVERLAY（弹窗挂在应用窗口根节点，应用内路由切换不隐藏），isModal 为 true（有蒙层、蒙层区域不透传事件），autoCancel 为 true（点蒙层关闭），maskRect 覆盖整窗，maskColor 为 0x33000000；levelMode 设为 EMBEDDED 时弹窗挂在 Page 或 NavDestination 下，immersiveMode 默认 DEFAULT 时蒙层按父节点布局约束显示，设为 EXTEND 才扩到状态栏和导航条。〔成立范围：levelMode 只在 showInSubWindow 为 false 时生效，immersiveMode 只在 EMBEDDED 时生效，showInSubWindow 为 true 时 maskRect 不生效（文档）。依据：@ohos.promptAction.d.ts 的 BaseDialogOptions 中 levelMode、immersiveMode、isModal、autoCancel 的 @default；maskColor、maskRect 默认值与枚举含义依据是 promptAction 文档说明（声明里没有 @default）。CustomDialogController 的 maskColor 默认同为 0x33000000（自定义弹窗文档）。〕
- 〔做法第 1 步〕安卓对话框主题未另设时 backgroundDimEnabled 为 true、backgroundDimAmount 为 0.6（框架 Theme、Theme.Holo、Theme.Material 及其 Light 变体；AppCompat 的 Platform.AppCompat 显式设 0.6），对话框窗口以 FLAG_DIM_BEHIND 把它后面的全部内容压暗，包括宿主 Activity 的底部 Tab 栏；鸿蒙自定义弹窗默认蒙层 0x33000000 只约 20% 黑，比安卓默认浅。〔成立范围：平台资源 android-30、36、37.0 一致，appcompat 1.1.0、1.8.0 一致；主题没写 backgroundDimEnabled 时 PhoneWindow 取 windowIsFloating 的值（对话框主题为 true，AppCompat 对话框主题显式写 true）；压暗范围依据是 WindowManager.LayoutParams#FLAG_DIM_BEHIND 的注释说明。不成立：Theme.Holo.Dialog.NoFrame、Theme.Material.Dialog.NoFrame 显式关闭压暗；手表（values-watch 的对话框主题 backgroundDimEnabled 为 false）；Theme.DeviceDefault 系列可由厂商定制，不保证为 0.6；应用在主题或代码里改了 dimAmount 时随应用。〕
