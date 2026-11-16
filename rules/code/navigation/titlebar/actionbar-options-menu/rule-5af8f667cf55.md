# showAsAction 带 withText 时文字只在宽屏显示，ActionBar 高度和标题字号随横竖屏切换

审的是：代码
触发（任一种）：
- 读到：菜单项 android:showAsAction="ifRoom|withText" 且有 android:icon，主题是 android:Theme.Holo；写错的样子：竖屏窄屏也恒显示图标加文字；标题栏 .height(48) 和标题字号写死，没有横屏取值
适用范围：目标端自绘的 Holo ActionBar 里动作项文字、栏高和标题字号
做法：
- 动作项文字只在窗口宽 ≥480vp 时显示（源端 values-w480dp 的 config_allowActionMenuItemTextWithIcon），样式按 TextAppearance.Holo.Widget.ActionBar.Menu：12fp、FontWeight.Bold、全大写；窄屏只显示图标
- 栏高和标题字号按横竖屏取值（竖屏 48 / 18，横屏 40 / 16），随窗口尺寸切换；窗口宽高可由应用壳根容器的 onAreaChange 写入共享状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextAppearance.Holo.Widget.ActionBar.Menu：textSize 12sp、textStyle bold、textAllCaps = @bool/config_actionMenuItemAllCaps：动作项文字样式（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，TextAppearance.Holo.Widget.ActionBar.Menu（按应用的 compileSdk 取对应平台））
- <bool name="config_actionMenuItemAllCaps">true</bool>：动作项文字全大写（出处：Android SDK 平台资源 data/res/values/config.xml，config_actionMenuItemAllCaps（按应用的 compileSdk 取对应平台））
- action_bar_default_height 48dip / values-land 40dip；action_bar_title_text_size 18dp / values-land 16dp：横竖屏的栏高和标题字号（出处：Android SDK 平台资源 data/res/values*/dimens.xml，action_bar_default_height、action_bar_title_text_size（按应用的 compileSdk 取对应平台））
- shouldAllowTextWithIcon()：screenWidthDp >= 480，或宽 ≥640 且高 ≥480，或横屏时允许 withText 文字：新版框架里显示文字的条件（横屏也显示）（出处：com.android.internal.view.menu.ActionMenuItemView#shouldAllowTextWithIcon）
- 宽 ≥480vp 时显示 12fp 粗体大写文字、横竖屏取 40/48 高与 16/18 标题后，横屏外观与源端一致：修复用的写法（出处：卡里修好并验证过）
未核实：条件按卡里的 values-w480dp 写；本机框架源码另把横屏也算进去，见 conflicts
来源：1 张卡，1 个应用
- case-5f607109511beae4aec1（Blockinger）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 5 ← 诊断
