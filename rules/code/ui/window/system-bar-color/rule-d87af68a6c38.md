# 入口 Ability 开系统栏时，同处用 setWindowSystemBarProperties 设源端状态栏色

审的是：代码
触发（任一种）：
- 读到：源端生效主题提供 statusBarColor（Material 系为 ?attr/colorPrimaryDark），窗口非全屏；写错的样子：EntryAbility 的 onWindowStageCreate 里只有 setWindowLayoutFullScreen(false) 和 setWindowSystemBarEnable(...)，没有 setWindowSystemBarProperties，运行时是系统默认的状态栏色；注释写「与源端一致」却只依据 values/styles.xml
适用范围：目标保持非全屏、源端状态栏底色由生效主题提供时，入口 Ability 里设置系统栏的那段代码
做法：
- 在 setWindowSystemBarEnable 之后同一处调 windowClass.setWindowSystemBarProperties({ statusBarColor: <源端状态栏底色 '#AARRGGBB'>, statusBarContentColor: <源端图标色> })；底色取生效主题 statusBarColor 解析出的值，暗底时图标色写 '#FFFFFFFF'
- 只读了 values/styles.xml、没查 values-vNN 覆盖时，不写「与源端一致」这类注释
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设主窗口状态栏属性；子窗口调用不生效，自由悬浮、分屏等非全屏/最大化模式下配置不生效（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties；arkts-apis-window-Window.md，setWindowSystemBarProperties）
- statusBarColor?: string，入参是十六进制 RGB 或 ARGB，如 '#FF00FF00'：状态栏背景色，不设时是系统配置的颜色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.statusBarColor；arkts-apis-window-i.md，SystemBarProperties）
- statusBarContentColor?: string，默认 '#E5FFFFFF'；设了它 isStatusBarLightIcon 就无效：状态栏文字和图标色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.statusBarContentColor；arkts-apis-window-i.md，SystemBarProperties）
- <item name="statusBarColor">?attr/colorPrimaryDark</item>：Material 系主题状态栏底色的来源（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light 的 statusBarColor（按应用的 compileSdk 取对应平台））
- Material 系里只有 Theme.Material.Light.LightStatusBar 把 windowLightStatusBar 设为 true：生效主题没设 windowLightStatusBar 时状态栏图标是浅色，目标图标色写白（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light.LightStatusBar；data/res/values/attrs.xml，windowLightStatusBar（按应用的 compileSdk 取对应平台））
- setWindowSystemBarEnable 后调用 setWindowSystemBarProperties({ statusBarColor, statusBarContentColor }) 状态栏颜色与源端一致；同时试设导航栏色无效：修好后的接法和观察到的行为（出处：卡里修好并验证过）
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties, callback: AsyncCallback<void>): void：同族接口：回调形式（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- getWindowSystemBarProperties(): SystemBarProperties：同族接口：读回当前系统栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowSystemBarProperties）
针对本应用要查的：
- 源端状态栏底色：源工程 values-vNN/styles.xml 里生效主题的 statusBarColor 或 colorPrimaryDark；没覆写时平台 themes_material.xml 里父主题的同名 item；顺着 @color/… 解析到 #AARRGGBB，作 statusBarColor 的值
来源：1 张卡，1 个应用
- case-1a1c2ec5cf0140821002（Sokoban）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 6 ← 诊断
