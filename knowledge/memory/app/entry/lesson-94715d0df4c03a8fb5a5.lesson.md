# 源 Activity 未声明 configChanges 时，旋转（未被 screenOrientation 锁定）、语言、深浅色、字号、显示大小变化都会重建它：目标 UIAbility 与页面不重建，逐页按源端重建时序显式处理——直接 show() 的非托管对话框关闭、托管对话框以新实例重显（setter 注入的监听与参数丢失）、文案与一次性状态刷新、新实例 onCreate/onResume 的可见效果重放；configChanges 不含 orientation 时旋转同样重建

ID：`lesson-94715d0df4c03a8fb5a5` · 版本：5

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-94715d0df4c03a8fb5a5.json` 改了 3 句，后面接了 14 条已核实的平台事实。原文、来源和证据卡见 [memory/app/entry/lesson-94715d0df4c03a8fb5a5.lesson.md](../../../../memory/app/entry/lesson-94715d0df4c03a8fb5a5.lesson.md)。

## 何时使用

规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期，以及资源文案与一次性状态的缓存时；为只有静态列表与弹窗的页面写配置变化行为时

## 适用情境

源 Activity 在 AndroidManifest 中未声明 android:configChanges，实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化时不重建，只回调 onConfigurationUpdate 或发出 display 'change'。 也包括页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框（不经 DialogFragment、showDialog 或 DialogPreference），目标用页内状态驱动的浮层承载，页面没有动态文案。 也包括 configChanges 已声明但不含 orientation（如只写 screenSize），Activity 持有 SurfaceView 与自建渲染线程，监听器里用 setBackgroundResource/setImageResource 等代码设置界面状态。 也包括源界面是 Compose（setContent），组合内以 LaunchedEffect(key)、remember 或 BoxWithConstraints 读取窗口约束做一次性计算（如按宽度算格数、列数），ViewModel 跨重建存活；目标在启动或重放中调用设置应用语言的接口（setLanguage、setAppPreferredLanguage）；页面用 getStringSync 等把资源文案取成字符串存进状态。

## 原因

未声明 configChanges 时，除被 screenOrientation 锁定的旋转外，语言、uiMode、fontScale、densityDpi 变化都会销毁并重建 Activity（mcc/mnc 自 Android 8.0 起默认不重建，只有写进 recreateOnConfigChanges 才重建）：旧实例存档，新 View 重新构造并重置一次性状态，再读档、按新配置重读文案与重算布局，对话框随旧窗口消失。把 onSaveInstanceState 只当作进程回收恢复，或假设切语言会触发尺寸回调，目标端切语言后仍显示旧文案与旧状态。重建后直接 show() 的非托管对话框随旧窗口消失，DialogFragment、showDialog、DialogPreference 托管的对话框会恢复，但恢复的是框架用无参构造新建、重跑 onCreateDialog 的新实例：只有 setArguments、对话框自身 onSaveInstanceState 与视图自存状态（如 EditText 文字）保留，经 setter 或构造参数注入的监听器、路径、标题为空，重显后内容回到默认、按钮可能只剩关闭；新 Activity 实例还会重跑 onCreate（含 savedInstanceState 分支）、onStart、onResume 的全部语句（重读持久数据刷新显示、复位导航或计数字段、按启动 Intent 再次弹窗）。目标页面旋转时不重建，页内浮层状态一直为真，对话框残留。规格只把“无 configChanges、无 screenOrientation”记成溯源事实时，没有人写关闭路径。 configChanges 不含 orientation 时，旋转同样销毁重建 Activity。重建时还在运行的东西各有结果：SurfaceView 的渲染线程仍在跑时，surface 随旧窗口失效，源端 lockCanvas 后不判空就崩溃，此时旋转的结果是崩溃；线程已结束才是关对话框、新实例重开。代码设置、没进 onSaveInstanceState 的视图属性，重建后回到布局初值。

## 做法

1. 规格逐个 Activity（不论页面是否有动态文案）读 configChanges 与 screenOrientation；未声明时把旋转与上述配置变化即重建写成生命周期验收：列出重建后哪些可见状态消失（直接 show() 的对话框）、哪些以新实例重显（托管对话框：逐个列出 setArguments、自身 onSaveInstanceState 与视图自存状态保留的内容，setter 或构造参数注入的字段为空，写出重显后的内容与按钮效果），并写明重建时序（关闭对话框 → 存档 → 重建一次性状态 → 读档 → 重读资源、重算布局 → 新实例重跑 onCreate（含恢复分支）、onStart、onResume），把这些生命周期语句的可见效果逐条写进验收。 configChanges 已声明但不含 orientation（如只写 screenSize）时，旋转同样按重建写验收。先按运行态拆分（渲染线程在跑或已结束、对话框是否显示）再分别写重建后果：仍在跑的 SurfaceView 渲染线程按 lesson-4da9eabca745b3b2be91 处理；代码设置且未存档的视图属性（如点击回调里 setBackgroundResource）列入重建后消失的可见状态。 源端界面是 Compose（setContent）时，重建等于整棵组合重新进入，不是一次重组：非 Saveable 的 remember 复位，LaunchedEffect、DisposableEffect 与 remember(key) 不论键是否变化都随首次组合再跑一次，读到新窗口约束（BoxWithConstraints 的 maxWidth、LocalConfiguration），“键不变就不重跑”只在同一组合内成立；把这些首次组合副作用的可见结果（如按新宽度重算的格数、列数）写进重建验收，判据给出转屏前后两个宽度下的期望值。组合副作用排在新实例 onCreate 体内语句之后（见 lesson-97966205ebe707e2e535）。
2. 实现时在 EntryAbility.onConfigurationUpdate 比较相关字段（language、colorMode、fontSizeScale、fontWeightScale、screenDensity；mcc/mnc 只在源 Activity 的 recreateOnConfigChanges 写了它们时才比较），显示大小变化另订阅 display.on('change') 比较密度，变化时显式通知页面按上述时序刷新；应用字号默认不跟随系统（configuration profile 里 fontSizeScale 缺省为 nonFollowSystem），源端跟随系统字号时先声明 followSystem，再在回调里比较 fontSizeScale。 onConfigurationUpdate 不等于配置真实变化：应用自己调用 ApplicationContext.setLanguage、i18n.System.setAppPreferredLanguage（含 onCreate 首帧前套用偏好语言、重放里重套语言）即使值没变也会同步回调它，回调里的 language 写法还可能与 context.config 不同（如 en 与 en-Latn-US）。比较基线在启动套用语言之前记录；回调入口把语言归一到语言子标签再比较，未变直接返回，变了先更新基线再执行重放；不比较或基线更新晚于重放都会无限递归（冷启动栈溢出）。在系统回调里调用其他可能改动同一配置的接口前，同样先确认它会不会同步触发该回调。
3. 源 View 在构造、尺寸变化或绘制时读取的资源文案与一次性状态，在映射中标注“随配置重建刷新”，不靠尺寸回调顺带刷新。 目标页面里 $r 渲染期文本会随语言自动刷新，用 getStringSync 等代码内取值存进状态或作 string 参数下传的文案快照不会：每个快照点在本页挂配置变化通知重取（或改为渲染期取值）；要交给重放切片时，在占位登记与交接里写出字段、取值函数与文件位置，不并入“$r 自动重解析”。
4. 页内状态驱动的浮层承载源端非托管对话框时补配置变化关闭路径：页面根容器 onAreaChange 判断横竖翻转，或由 onConfigurationUpdate 通知页面，关闭这些浮层并保留列表等其余状态。 代码设置的视图属性也在这条路径上复位到布局初值。托管对话框对应的弹层在同一路径上改用重建后的内容与回调，不原样保留原回调；新实例 onCreate/onResume 语句的可见效果（刷新显示、复位字段、按启动 Intent 再弹窗）也在这条路径上重放。 源端重建后按新尺寸重跑的首次计算（如按容器宽度算格数）挂到 onAreaChange 的宽度变化上：首次测量照常触发，之后旧宽大于 0 且新旧宽不同才再算。

## 可选检查

- 运行中分别切换系统语言、深浅色、字号与显示大小，对照两端的画布文案、帮助文案、对话框与状态栏底色。
- 说明对话框打开时旋转，两端都只剩列表、对话框关闭。

## 已核实的平台事实

核实时用的是 API 23（HarmonyOS 6.1.0，SDK ets 6.1.0.105）；文档用 2026-05 的 OpenHarmony 中文文档副本；安卓 平台资源 android-34；源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看。

- 〔原因 / 做法第 1 步〕configChanges 没列出的配置变化发生时 Activity 被重启，列出的改为回调 onConfigurationChanged；重启即走 onPause、onStop、onDestroy，再用 onSaveInstanceState 存下的 savedInstanceState 新建实例（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges；android.app.Activity（类注释 Configuration Changes 一节））
- 〔做法第 1、2 步〕configChanges 取值：locale、uiMode、fontScale、fontWeightAdjustment、density、orientation、screenSize 等；横竖切换时 screenSize 也变（targetSdk ≥ 13），旋转不重建要两者都声明；mcc、mnc 自 Android 8.0 起未声明也不重建，要重建须写进 recreateOnConfigChanges（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的各 flag、recreateOnConfigChanges）
- 〔原因 / 做法第 1 步〕Activity#showDialog 托管的对话框首次调 onCreateDialog，此后自动存档恢复（args 也存）；Activity 销毁时 handleDestroyActivity 对其 token 执行 closeAll，直接 show() 的对话框窗口被移除（出处：android.app.Activity#showDialog(int, Bundle)；android.app.ActivityThread#handleDestroyActivity）
- 〔原因 / 做法第 1 步〕Fragment 恢复状态时用公开无参构造重新实例化（androidx 的 FragmentFactory.instantiate 也是 getConstructor().newInstance()），带参构造不被调用；setArguments 的参数跨重建保留；EditText#getFreezesText 恒为 true（出处：android.app.Fragment#Fragment()、#setArguments；androidx.fragment:fragment 1.8.9，FragmentFactory.instantiate（字节码）；android.widget.EditText#getFreezesText）
- 〔做法第 1 步〕ComponentActivity.setContent 先看窗口内容区第一个子视图是不是 ComposeView，不是就新建 ComposeView 再 setContent：重建后的新 Activity 实例是新窗口，组合从头进入（出处：androidx.activity:activity-compose 1.13.0，ComponentActivityKt.setContent（字节码）；android.app.Activity（类注释 Configuration Changes 一节））
- 〔原因 / 做法第 2 步〕UIAbility（继承 Ability）的 onConfigurationUpdate(newConfig: Configuration): void 在环境变量变化时回调，不重启 UIAbility；Configuration 字段均可选：language、colorMode、direction、screenDensity、displayId、fontSizeScale、fontWeightScale、mcc、mnc、locale 等（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate；ets/api/@ohos.app.ability.Configuration.d.ts，Configuration；文档 subscribe-system-environment-variable-changes.md，在UIAbility组件中订阅回调）
- 〔做法第 2 步〕应用字号默认不跟随系统：app.json5 的 "configuration": "$profile:configuration"，profile 里 fontSizeScale 取 followSystem 才跟随（缺省 nonFollowSystem）；调 setFontSizeScale 后也不再跟随（出处：文档 app-configuration-file.md，configuration标签；subscribe-system-environment-variable-changes.md，设置字体大小）
- 〔做法第 2 步〕display.on('change', callback: Callback<number>)：显示设备改变（如方向改变）时回调 displayId；用 getDisplayByIdSync(displayId) 或 getDefaultDisplaySync() 取 Display，比较 densityPixels、densityDPI（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.on、display.getDisplayByIdSync、Display.densityPixels；文档 js-apis-display.md，display.on('add'|'remove'|'change')）
- 〔做法第 2 步〕ApplicationContext.setLanguage(language: string): void，设后不再能订阅系统语言变化；static i18n.System.setAppPreferredLanguage(language: string): void 设后优先加载该语言资源，设为 'default' 才跟随系统语言、冷启动生效（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.setLanguage；ets/api/@ohos.i18n.d.ts，System.setAppPreferredLanguage；文档 subscribe-system-environment-variable-changes.md，设置应用语言；js-apis-i18n.md，setAppPreferredLanguage）
- 〔做法第 2 步〕调用 setLanguage 或 setAppPreferredLanguage 会同步回调 onConfigurationUpdate，值没变也回调；回调里的 language 写法可能与 context.config 不同（如 en 与 en-Latn-US）；系统显示大小变化不回调 onConfigurationUpdate，会触发 display 'change'，densityPixels 随之变化（出处：卡里修好并验证过）
- 〔做法第 3 步〕ResourceManager.getStringSync(resId: number): string 按调用时的配置取一次字符串；getStringSync(resource: Resource) 自 API 20 起废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- 〔做法第 3 步〕系统语言切换后，$r 渲染的文本自动按新语言刷新；用 getStringSync 取出存进状态的字符串保持旧值（出处：卡里修好并验证过）
- 〔做法第 4 步〕onAreaChange(event: (oldValue: Area, newValue: Area) => void): T，组件区域变化时回调；Area.width: Length，单位 vp（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange；ets/component/units.d.ts，Area.width；文档 ts-types.md，Area）
- 〔做法第 4 步〕转屏时 UIAbility 与页面都不重建，页内状态变量（如浮层显示标志）保持转屏前的值（出处：卡里修好并验证过）
