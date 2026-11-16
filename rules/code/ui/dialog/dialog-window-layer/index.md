# 对话框窗口层的遮罩、投影、圆角、宽度和位置

agent 会看到什么：读到源端用 AlertDialog、MaterialDialog、DialogPreference 或 android:theme 为 Theme.*.Dialog 的 Activity 弹出浮动窗口，外观来自主题（backgroundDimAmount、windowElevation、窗口宽度），窗口在系统栏之间居中、压暗应用画的状态栏；产物里 openCustomDialog 的 maskColor、alignment / offset，自绘卡片的 .shadow、.borderRadius、.width 和弹窗期间的 statusBarColor

## 规矩

- rule-aa8b1146baab｜Dialog 形态的源端控件迁成自绘弹窗时，补上窗口层的投影、遮罩、圆角和宽度｜读到：源端是 Dialog 形态（MaterialDialog、AlertDialog、DialogPreference），对话框主题属 Theme.MaterialComponents.Light.Dialog、Theme.AppCompat 一类；写错：目标 openCustomDialog 的弹窗只做了内容区：没有 shadow 投影，maskColor、圆角、宽度没按源端主题写
- rule-3f9cd80f0cad｜宿主 openCustomDialog 承载框架对话框时，maskColor 按主题遮罩浓度写｜读到：源端框架 AlertDialog 没改窗口 dim，运行期主题有 backgroundDimAmount（Theme.Material.Light 为 0.6）；写错：`openCustomDialog(content, { alignment, autoCancel, onDidDisappear })` 没有 maskColor
- rule-70c3297f6494｜Dialog 主题窗口的遮罩、底色、圆角按主题值写，不拿语义不同的颜色资源凑｜读到：Activity 的 android:theme 是 Theme.*.Dialog，工程 colors.xml 里另有半透明黑色等颜色资源；写错：遮罩写 .backgroundColor($r('app.color.…')) 借用语义不同的颜色资源，卡片底色和 .borderRadius(...) 取近似值，遮罩没有 onClick 点外关闭
- rule-a07930a251ea｜复刻平台对话框卡片要写 floating_window_z 投影，不因无截图就不写｜读到：源对话框用平台 Material 对话框主题（windowElevation 为 @dimen/floating_window_z）；写错：自绘对话框卡片只有底色和圆角，没有 .shadow(...)，注释写「无截图校准不写阴影」
- rule-0b0c89749563｜自绘对话框容器不写 width('100%') 或凭印象的百分比，按库或主题公式算 dialogWidth｜读到：源端用 material-dialogs 的 MaterialDialog.Builder（含 customView）弹窗；写错：自绘对话框根 Column 写 .width('100%') 交给 openCustomDialog，只设了 alignment，没有窗口宽度约束，运行时整屏宽
- rule-8668c07ca4c6｜弹窗用 DialogAlignment.Center 居中承载源对话框时，按上下避让差的一半加 offset｜读到：源端用 AlertDialog / Dialog 窗口弹出对话框（对话框窗口在状态栏与导航栏之间居中）；写错：openCustomDialog 写 alignment: DialogAlignment.Center，没有 offset，也没读主窗口的 TYPE_SYSTEM / TYPE_NAVIGATION_INDICATOR 避让
- rule-fdfb03a7f4d7｜源主题由应用窗口画状态栏底色且目标非全屏时，弹窗期间把 statusBarColor 切成压暗色｜读到：源端用 AlertDialog / Dialog 窗口，应用主题是 Theme.Material 及以后（windowDrawsSystemBarBackgrounds=true，statusBarColor=?attr/colorPrimaryDark 且不透明），对话框按 backgroundDimAmount 压暗；写错：openCustomDialog 只写了 maskColor（如按 dim 0.6 得到的 `#99000000`），onWillAppear / onWillDisappear 里没有切主窗口的状态栏底色
