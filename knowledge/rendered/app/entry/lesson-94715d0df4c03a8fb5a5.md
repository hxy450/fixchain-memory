# 源 Activity 未声明 configChanges 时，旋转（未被 screenOrientation 锁定）、语言、深浅色、字号、显示大小变化都会重建它：目标 UIAbility 与页面不重建，逐页按源端重建时序显式处理——直接 show() 的非托管对话框关闭、托管对话框以新实例重显（setter 注入的监听与参数丢失）、文案与一次性状态刷新、新实例 onCreate/onResume 的可见效果重放；configChanges 不含 orientation 时旋转同样重建

## 何时使用

规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期，以及资源文案与一次性状态的缓存时；为只有静态列表与弹窗的页面写配置变化行为时

## 适用情境

源 Activity 在 AndroidManifest 中未声明 android:configChanges，实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化时不重建，只回调 onConfigurationUpdate 或发出 display 'change'。 也包括页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框（不经 DialogFragment、showDialog 或 DialogPreference），目标用页内状态驱动的浮层承载，页面没有动态文案。 也包括 configChanges 已声明但不含 orientation（如只写 screenSize），Activity 持有 SurfaceView 与自建渲染线程，监听器里用 setBackgroundResource/setImageResource 等代码设置界面状态。 也包括源界面是 Compose（setContent），组合内以 LaunchedEffect(key)、remember 或 BoxWithConstraints 读取窗口约束做一次性计算（如按宽度算格数、列数），ViewModel 跨重建存活；目标在启动或重放中调用设置应用语言的接口（setLanguage、setAppPreferredLanguage）；页面用 getStringSync 等把资源文案取成字符串存进状态。

## 原因

未声明 configChanges 时，除被 screenOrientation 锁定的旋转外（Android 16 起 targetSdk≥36 的应用在最小宽度 ≥600dp 的大屏上，portrait、landscape 及其 reverse、sensor、user 变体的锁定按 unspecified 处理，旋转照样重建），语言、uiMode、fontScale、densityDpi 变化都会销毁并重建 Activity（mcc/mnc 自 Android 8.0 起默认不重建，只有写进 recreateOnConfigChanges 才重建）：旧实例存档，新 View 重新构造并重置一次性状态，再读档、按新配置重读文案与重算布局，对话框随旧窗口消失。把 onSaveInstanceState 只当作进程回收恢复，或假设切语言会触发尺寸回调，目标端切语言后仍显示旧文案与旧状态。重建后直接 show() 的非托管对话框随旧窗口消失，DialogFragment、showDialog、DialogPreference 托管的对话框会恢复，但恢复的是框架用无参构造新建（androidx 应用没有另设 FragmentFactory 时）、重跑 onCreateDialog 的新实例：只有 setArguments、对话框自身 onSaveInstanceState 与视图自存状态（如 EditText 文字）保留，经 setter 或构造参数注入的监听器、路径、标题为空，重显后内容回到默认、按钮可能只剩关闭；新 Activity 实例还会重跑 onCreate（含 savedInstanceState 分支）、onStart、onResume 的全部语句（重读持久数据刷新显示、复位导航或计数字段、按启动 Intent 再次弹窗）。目标页面旋转时不重建，页内浮层状态一直为真，对话框残留。规格只把“无 configChanges、无 screenOrientation”记成溯源事实时，没有人写关闭路径。 configChanges 不含 orientation 时，旋转同样销毁重建 Activity。重建时还在运行的东西各有结果：SurfaceView 的渲染线程仍在跑时，surface 随旧窗口失效，源端 lockCanvas 后不判空就崩溃，此时旋转的结果是崩溃；线程已结束才是关对话框、新实例重开。代码设置、没进 onSaveInstanceState 的视图属性，重建后回到布局初值。 同一窗口里的视图状态按视图类自己的存档决定：Activity 的 onSaveInstanceState / onRestoreInstanceState 走默认实现或调了 super 时，带 id、实现了 onSaveInstanceState 的视图在新实例里按 id 恢复（如 DrawerLayout 的打开抽屉、EditText 的文字），旋转后仍是原样，目标对应的抽屉、侧栏、输入框保持不动；直接 show() 的对话框（独立窗口）和代码设置且没存档的属性才走关闭 / 复位路径（托管对话框按上文以新实例重显）。拿不准时先查该视图类的 onSaveInstanceState。

## 做法

1. 规格逐个 Activity（不论页面是否有动态文案）读 configChanges 与 screenOrientation；未声明时把旋转与上述配置变化即重建写成生命周期验收：列出重建后哪些可见状态消失（直接 show() 的对话框）、哪些以新实例重显（托管对话框：逐个列出 setArguments、自身 onSaveInstanceState 与视图自存状态保留的内容，setter 或构造参数注入的字段为空，写出重显后的内容与按钮效果），并写明重建时序（关闭对话框 → 存档 → 重建一次性状态 → 读档 → 重读资源、重算布局 → 新实例重跑 onCreate（含恢复分支）、onStart、onResume），把这些生命周期语句的可见效果逐条写进验收。 configChanges 已声明但没有同时含 orientation 与 screenSize（如只写 screenSize，或 targetSdk≥13 时只写 orientation）时，旋转同样按重建写验收。先按运行态拆分（渲染线程在跑或已结束、对话框是否显示）再分别写重建后果：仍在跑的 SurfaceView 渲染线程按 lesson-4da9eabca745b3b2be91 处理；代码设置且未存档的视图属性（如点击回调里 setBackgroundResource）列入重建后消失的可见状态。 源端界面是 Compose（setContent）时，重建等于整棵组合重新进入，不是一次重组：非 Saveable 的 remember 复位，LaunchedEffect、DisposableEffect 与 remember(key) 不论键是否变化都随首次组合再跑一次，读到新窗口约束（BoxWithConstraints 的 maxWidth、LocalConfiguration），“键不变就不重跑”只在同一组合内成立；把这些首次组合副作用的可见结果（如按新宽度重算的格数、列数）写进重建验收，判据给出转屏前后两个宽度下的期望值。组合副作用排在新实例 onCreate 体内语句之后（见 lesson-97966205ebe707e2e535）。
2. 实现时在 EntryAbility.onConfigurationUpdate 比较相关字段（language、colorMode、fontSizeScale、fontWeightScale、screenDensity；mcc/mnc 只在源 Activity 的 recreateOnConfigChanges 写了它们时才比较），显示大小变化另订阅 display.on('change') 比较密度，变化时显式通知页面按上述时序刷新；应用字号默认不跟随系统（configuration profile 里 fontSizeScale 缺省为 nonFollowSystem），源端跟随系统字号时先声明 followSystem，再在回调里比较 fontSizeScale。 onConfigurationUpdate 不等于配置真实变化：应用自己调用 ApplicationContext.setLanguage、i18n.System.setAppPreferredLanguage（含 onCreate 首帧前套用偏好语言、重放里重套语言）即使值没变也会同步回调它，回调里的 language 写法还可能与 context.config 不同（如 en 与 en-Latn-US）。比较基线在启动套用语言之前记录；回调入口把语言归一到语言子标签再比较，未变直接返回，变了先更新基线再执行重放；不比较或基线更新晚于重放都会无限递归（冷启动栈溢出）。在系统回调里调用其他可能改动同一配置的接口前，同样先确认它会不会同步触发该回调。
3. 源 View 在构造、尺寸变化或绘制时读取的资源文案与一次性状态，在映射中标注“随配置重建刷新”，不靠尺寸回调顺带刷新。 目标页面里 $r 渲染期文本会随语言自动刷新，用 getStringSync 等代码内取值存进状态或作 string 参数下传的文案快照不会：每个快照点在本页挂配置变化通知重取（或改为渲染期取值）；要交给重放切片时，在占位登记与交接里写出字段、取值函数与文件位置，不并入“$r 自动重解析”。
4. 页内状态驱动的浮层承载源端非托管对话框时补配置变化关闭路径（同一窗口里带 id、自己存档的视图不在此列：如 DrawerLayout 的打开抽屉、EditText 的文字旋转后仍是原样，目标对应的抽屉、侧栏、输入框保持不动，不在这条路径上关闭或清空；拿不准时先查该视图类的 onSaveInstanceState）：页面根容器 onAreaChange 判断横竖翻转，或由 onConfigurationUpdate 通知页面（靠它感知旋转时，module.json5 里该 UIAbility 的 orientation 配成 auto_rotation），关闭这些浮层并保留列表等其余状态。 代码设置的视图属性也在这条路径上复位到布局初值。托管对话框对应的弹层在同一路径上改用重建后的内容与回调，不原样保留原回调；新实例 onCreate/onResume 语句的可见效果（刷新显示、复位字段、按启动 Intent 再弹窗）也在这条路径上重放。 源端重建后按新尺寸重跑的首次计算（如按容器宽度算格数）挂到 onAreaChange 的宽度变化上：首次测量照常触发，之后旧宽大于 0 且新旧宽不同才再算。

## 可选检查

- 运行中分别切换系统语言、深浅色、字号与显示大小，对照两端的画布文案、帮助文案、对话框与状态栏底色。
- 说明对话框打开时旋转，两端都只剩列表、对话框关闭。

来源支持：8 张卡 · 5 次迁移 · 5 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码；androidx 的 activity-compose、compose runtime、lifecycle-viewmodel、fragment 取 androidx-main 源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Activity 没有在 configChanges 里声明的配置变化（如旋转、语言、输入设备）发生时，当前 Activity 走 onPause、onStop、onDestroy 销毁；它在前台或可见时，随后用旧实例 onSaveInstanceState 生成的 savedInstanceState 新建一个实例；声明了的变化改为回调 onConfigurationChanged、不重启，但一次变化里只要含一项未声明的仍会重启
- 〔原因 / 做法第 1 步〕configChanges 的取值：locale（语言）、uiMode（含深浅色）、fontScale（字号）、fontWeightAdjustment（字重）、density（显示密度，含显示大小）、orientation 0x0080（用户旋转设备）、screenSize 0x0400（当前可用屏幕尺寸，横竖切换时也变）；targetSdk 达到 13（HONEYCOMB_MR2）的应用旋转时 orientation 与 screenSize 同时变，只写其中一项仍会因旋转重建；configChanges 里的 colorMode 指色域或动态范围，深浅色属于 uiMode
- 〔原因〕configChanges 没写 mcc、mnc 时，自 Android 8.0（O）起也不因 SIM 的 mcc、mnc 变化重建 Activity；要重建须写进 recreateOnConfigChanges
- 〔原因〕screenOrientation：targetSdk ≥ 36（Android 16）的应用在最小宽度 ≥ 600dp 的设备上，portrait、landscape、reversePortrait、reverseLandscape、sensorPortrait、sensorLandscape、userPortrait、userLandscape 被系统忽略，按 unspecified 处理；设备厂商也可配置忽略该属性
- 〔原因 / 做法第 1 步〕onSaveInstanceState 对 targetSdk ≥ 28（P）的应用在 onStop 之后调用；更早的 targetSdk 在 onStop 之前调用，与 onPause 的先后不保证
- 〔原因 / 做法第 1 步〕Activity.showDialog(id, args) 托管的对话框由 Activity 自动保存和恢复，args 也一并保存恢复（该接口已废弃，推荐 DialogFragment）
- 〔原因 / 做法第 1 步〕Fragment 必须有公开无参构造：恢复 Activity 状态时框架用它重新实例化 Fragment，带参构造不会被调用，参数只能经 setArguments 传入、getArguments 取回；androidx 的 Fragment 由默认 FragmentFactory 调无参构造，应用另设 FragmentFactory 才会走别的构造
- 〔原因 / 做法第 1 步〕DialogFragment 在自身 onSaveInstanceState 里存下对话框的 onSaveInstanceState（键 android:savedDialogState），重建后恢复到新建的对话框上；DialogPreference 在对话框显示时把 isDialogShowing 与对话框状态存进自身保存状态，恢复时重新 showDialog
- 〔原因 / 做法第 1、4 步〕视图状态只为有 id 且没有禁止保存的 View 存进 savedInstanceState；View.onSaveInstanceState 本身只存自动填充等少量状态，不存背景、图片等代码设置的属性；EditText 的 getFreezesText 恒为 true，文字随视图状态保存
- 〔原因 / 做法第 1 步〕源 Activity 未声明 configChanges、DialogFragment 的监听器和参数经 setter 写入字段时，安卓设备上转屏后对话框以默认内容重显：列表回到默认数据、无标题、点行无效、按钮只关闭，EditText 里已输入的文字保留
- 〔原因〕SurfaceHolder.lockCanvas() 在 surface 尚未创建或不能编辑时返回 null
- 〔原因〕SurfaceView 渲染线程在跑、run() 中 lockCanvas 后不判空就绘制时，安卓设备上旋转（Activity 重建）崩溃，进行中按返回、按 Home 也崩溃；循环已结束时旋转按重建重开
- 〔适用情境 / 做法第 1 步〕ComponentActivity.setContent 在 onCreate 里先给 ComposeView 设好内容再 setContentView，组合在 ComposeView 挂到窗口时才创建；Activity 的窗口在 onResume 执行完后才加进 WindowManager，所以首次组合及其中的副作用晚于 onCreate、onStart、onResume 里的语句
- 〔适用情境 / 做法第 1 步〕安卓设备上冷启动实测：onCreate 里 setContent 之后、onCreate 末尾才自增的启动计数，组合内 LifecycleEventEffect(ON_CREATE) 读到的是自增后的值
- 〔做法第 1 步〕LaunchedEffect 进入组合时启动协程，同一组合内以不同的键重组时取消并重新启动，离开组合时取消；remember 只在组合时计算，同一组合内的重组返回已存的值；rememberSaveable 存的值经 saved instance state 跨 Activity 重建和进程重建保留；Activity 重建时新实例的 setContent 建立一个新的组合
- 〔做法第 1 步〕ViewModel 由 ViewModelStoreOwner 持有，跨配置变化（如旋转）保留，直到所有者真正销毁
- 〔适用情境 / 做法第 2 步〕UIAbility.onConfigurationUpdate(newConfig) 在系统环境变量（语言、深浅色、屏幕方向等）变化时回调，从 newConfig 取最新值，UIAbility 不重启；这个回调随所在 UIAbility 的生命周期有效
- 〔做法第 2、4 步〕用 onConfigurationUpdate 监听屏幕方向变化时，module.json5 abilities 里该 UIAbility 的 orientation 要配成 auto_rotation
- 〔做法第 2 步〕应用在后台时环境变量变化，订阅通知延迟到应用回到前台才收到；configuration 标签里某项配成 nonFollowSystem 时收不到该项的系统变化
- 〔做法第 2 步〕Configuration 的字段都可选：language、colorMode、direction、screenDensity、fontSizeScale、fontWeightScale（这两项 API 12 起，默认值为 1）、mcc、mnc（API 12 起）、locale（Intl.Locale，API 20 起）
- 〔做法第 2 步〕应用字体大小默认不跟随系统：app.json5 的 configuration 标签指向的 profile 里 fontSizeScale 可缺省，缺省为 nonFollowSystem，配 followSystem 才跟随；应用调用 setFontSizeScale 后也不跟随系统、不能再订阅系统字号变化
- 〔做法第 2 步〕ApplicationContext.setLanguage(language)（API 11 起）只能在主线程调用，要在窗口创建完成、页面 loadContent 之后调用；调用后系统语言再变化，onConfigurationUpdate 不再因此触发
- 〔做法第 2 步〕i18n.System.setAppPreferredLanguage(language)（API 11 起）设置后应用优先加载该语言的资源；设为 'default' 时跟随系统语言，冷启动后生效
- 〔做法第 2 步〕应用在启动时或 onConfigurationUpdate 里调用 ApplicationContext.setLanguage、i18n.System.setAppPreferredLanguage 时，即使语言值没变，设备上也同步回调 onConfigurationUpdate；回调里 newConfig.language 为 en，而启动时 context.config 里是 en-Latn-US；回调里无条件再设语言会递归，冷启动时栈溢出崩溃
- 〔做法第 2 步〕display.on('change', callback) 在显示设备改变时回调，参数是 displayId；display.getDisplayByIdSync(displayId)（API 12 起）按 id 取 Display；Display.densityPixels 是物理像素与逻辑像素的缩放系数
- 〔做法第 2 步〕设备上改“显示大小”时只发出 display 'change'，不触发 onConfigurationUpdate、windowSizeChange、avoidAreaChange（SDK 声明和文档没有写明这一点）
- 〔做法第 3 步〕resourceManager.getStringSync(resId) 按资源 ID 同步返回一个 string；getStringSync(resource: Resource) 自 API 20 起废弃
- 〔做法第 3 步〕运行中切换应用语言后，$r 渲染的文本按新语言显示，用 getStringSync 取出存进状态的文案保持旧语言
- 〔原因 / 做法第 3 步〕目标 UIAbility 在切换系统语言后不重建：页面构造时取好的画布文案、帮助文案和打开着的确认框都保持切换前的状态；只在 onAreaChange 里重取文案的页面，切语言后画布仍是旧语言
- 〔做法第 4 步〕onAreaChange((oldValue: Area, newValue: Area) => void) 只在布局变化导致组件大小、位置变化时回调，translate、offset、scale、transform 等绘制属性变化不回调；Area.width、Area.height 是组件宽高
- 〔做法第 4 步〕目标页面在旋转时不重建：页内状态驱动的浮层旋转后仍显示；只在首次测量时按宽度做的计算，转横屏后保持竖屏时的结果
- 〔做法第 4 步〕PromptAction.openCustomDialog(dialogContent, options?) 用 ComponentContent 打开自定义弹窗，closeCustomDialog(dialogContent) 关闭；updateCustomDialog(dialogContent, options) 只更新已弹出弹窗的样式，目前仅支持 alignment、offset、autoCancel、maskColor；ComponentContent.update(args) 更新其 builder 函数的参数（API 12 起）
