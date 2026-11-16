# 源主题按明暗设状态栏图标极性时，statusBarContentColor 随主题下发，不写死白色

审的是：代码
触发（任一种）：
- 读到：源端主题在组合期设 isAppearanceLightStatusBars = isLight，有深浅两套配色；写错的样子：窗口初始化把 statusBarContentColor / navigationBarContentColor 写死为 '#FFFFFF'，或壳层的写死值覆盖了主题服务的设置
适用范围：源端状态栏图标明暗随主题切换、目标端用 setWindowSystemBarProperties 设图标色时
做法：
- statusBarContentColor、navigationBarContentColor 随主题取：浅色主题（isLight 为 true）写深色图标色，深色主题写浅色；用 mainWindow.setWindowSystemBarProperties({ statusBarContentColor, navigationBarContentColor }) 下发
- 极性只由主题服务统一下发，壳层删掉写死值，不再覆盖
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：Window 上设状态栏、导航条属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- statusBarContentColor?: string；navigationBarContentColor?: string：SystemBarProperties 里状态栏、导航条的内容（图标文字）颜色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.statusBarContentColor）
- APPEARANCE_LIGHT_STATUS_BARS：浅色状态栏时改前景色，让栏上内容看得清：源端 isAppearanceLightStatusBars 为 true 即浅色栏配深色图标（出处：android.view.WindowInsetsController#APPEARANCE_LIGHT_STATUS_BARS）
- getWindowSystemBarProperties(): SystemBarProperties：同族接口：读回当前系统栏属性，只支持主窗口（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowSystemBarProperties）
- setSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>（since 9 弃用）：同族接口：旧接口，改用 setWindowSystemBarProperties（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setSystemBarProperties）
针对本应用要查的：
- isLight 的判定和两套主题下的图标极性：源工程 Compose 主题文件里设 isAppearanceLightStatusBars 的那段，以及决定 isLight 的主题模式判断；isLight 为 true 时目标写深色图标色，否则写浅色
未核实：isAppearanceLightStatusBars 属于 androidx.core，库代码本机没有源码，语义按平台的 APPEARANCE_LIGHT_STATUS_BARS 核
来源：1 张卡，1 个应用
- case-b3c176b95cabcc03a434（jerboa）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断
