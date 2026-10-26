# 源 Activity 未声明 configChanges 时，旋转（未被 screenOrientation 锁定）、语言、深浅色、字号、显示大小变化都会重建它：目标 UIAbility 与页面不重建，逐页按源端重建时序显式处理——直接 show() 的非托管对话框关闭、托管对话框以新实例重显（setter 注入的监听与参数丢失）、文案与一次性状态刷新、新实例 onCreate/onResume 的可见效果重放；configChanges 不含 orientation 时旋转同样重建

ID：`lesson-94715d0df4c03a8fb5a5` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期，以及资源文案与一次性状态的缓存时；为只有静态列表与弹窗的页面写配置变化行为时

## 适用情境

源 Activity 在 AndroidManifest 中未声明 android:configChanges，实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化时不重建，只回调 onConfigurationUpdate 或发出 display 'change'。 也包括页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框（不经 DialogFragment、showDialog 或 DialogPreference），目标用页内状态驱动的浮层承载，页面没有动态文案。 也包括 configChanges 已声明但不含 orientation（如只写 screenSize），Activity 持有 SurfaceView 与自建渲染线程，监听器里用 setBackgroundResource/setImageResource 等代码设置界面状态。 也包括源界面是 Compose（setContent），组合内以 LaunchedEffect(key)、remember 或 BoxWithConstraints 读取窗口约束做一次性计算（如按宽度算格数、列数），ViewModel 跨重建存活；目标在启动或重放中调用设置应用语言的接口（setLanguage、setAppPreferredLanguage）；页面用 getStringSync 等把资源文案取成字符串存进状态。

## 原因

未声明 configChanges 时，除被 screenOrientation 锁定的旋转外，语言、uiMode、fontScale、densityDpi、mcc/mnc 变化都会销毁并重建 Activity：旧实例存档，新 View 重新构造并重置一次性状态，再读档、按新配置重读文案与重算布局，对话框随旧窗口消失。把 onSaveInstanceState 只当作进程回收恢复，或假设切语言会触发尺寸回调，目标端切语言后仍显示旧文案与旧状态。重建后直接 show() 的非托管对话框随旧窗口消失，DialogFragment、showDialog、DialogPreference 托管的对话框会恢复，但恢复的是框架用无参构造新建、重跑 onCreateDialog 的新实例：只有 setArguments、对话框自身 onSaveInstanceState 与视图自存状态（如 EditText 文字）保留，经 setter 或构造参数注入的监听器、路径、标题为空，重显后内容回到默认、按钮可能只剩关闭；新 Activity 实例还会重跑 onCreate（含 savedInstanceState 分支）、onStart、onResume 的全部语句（重读持久数据刷新显示、复位导航或计数字段、按启动 Intent 再次弹窗）。目标页面旋转时不重建，页内浮层状态一直为真，对话框残留。规格只把“无 configChanges、无 screenOrientation”记成溯源事实时，没有人写关闭路径。 configChanges 不含 orientation 时，旋转同样销毁重建 Activity。重建时还在运行的东西各有结果：SurfaceView 的渲染线程仍在跑时，surface 随旧窗口失效，源端 lockCanvas 后不判空就崩溃，此时旋转的结果是崩溃；线程已结束才是关对话框、新实例重开。代码设置、没进 onSaveInstanceState 的视图属性，重建后回到布局初值。

## 做法

1. 规格逐个 Activity（不论页面是否有动态文案）读 configChanges 与 screenOrientation；未声明时把旋转与上述配置变化即重建写成生命周期验收：列出重建后哪些可见状态消失（直接 show() 的对话框）、哪些以新实例重显（托管对话框：逐个列出 setArguments、自身 onSaveInstanceState 与视图自存状态保留的内容，setter 或构造参数注入的字段为空，写出重显后的内容与按钮效果），并写明重建时序（关闭对话框 → 存档 → 重建一次性状态 → 读档 → 重读资源、重算布局 → 新实例重跑 onCreate（含恢复分支）、onStart、onResume），把这些生命周期语句的可见效果逐条写进验收。 configChanges 已声明但不含 orientation（如只写 screenSize）时，旋转同样按重建写验收。先按运行态拆分（渲染线程在跑或已结束、对话框是否显示）再分别写重建后果：仍在跑的 SurfaceView 渲染线程按 lesson-4da9eabca745b3b2be91 处理；代码设置且未存档的视图属性（如点击回调里 setBackgroundResource）列入重建后消失的可见状态。 源端界面是 Compose（setContent）时，重建等于整棵组合重新进入，不是一次重组：非 Saveable 的 remember 复位，LaunchedEffect、DisposableEffect 与 remember(key) 不论键是否变化都随首次组合再跑一次，读到新窗口约束（BoxWithConstraints 的 maxWidth、LocalConfiguration），“键不变就不重跑”只在同一组合内成立；把这些首次组合副作用的可见结果（如按新宽度重算的格数、列数）写进重建验收，判据给出转屏前后两个宽度下的期望值。组合副作用排在新实例 onCreate 体内语句之后（见 lesson-97966205ebe707e2e535）。
2. 实现时在 EntryAbility.onConfigurationUpdate 比较相关字段（language、colorMode、fontSizeScale、fontWeightScale、screenDensity、mcc/mnc），显示大小变化另订阅 display.on('change') 比较密度，变化时显式通知页面按上述时序刷新；字号变化只有在应用声明跟随系统字号后才会下发。 onConfigurationUpdate 不等于配置真实变化：应用自己调用 ApplicationContext.setLanguage、i18n.System.setAppPreferredLanguage（含 onCreate 首帧前套用偏好语言、重放里重套语言）即使值没变也会同步回调它，回调里的 language 写法还可能与 context.config 不同（如 en 与 en-Latn-US）。比较基线在启动套用语言之前记录；回调入口把语言归一到语言子标签再比较，未变直接返回，变了先更新基线再执行重放；不比较或基线更新晚于重放都会无限递归（冷启动栈溢出）。在系统回调里调用其他可能改动同一配置的接口前，同样先确认它会不会同步触发该回调。
3. 源 View 在构造、尺寸变化或绘制时读取的资源文案与一次性状态，在映射中标注“随配置重建刷新”，不靠尺寸回调顺带刷新。 目标页面里 $r 渲染期文本会随语言自动刷新，用 getStringSync 等代码内取值存进状态或作 string 参数下传的文案快照不会：每个快照点在本页挂配置变化通知重取（或改为渲染期取值）；要交给重放切片时，在占位登记与交接里写出字段、取值函数与文件位置，不并入“$r 自动重解析”。
4. 页内状态驱动的浮层承载源端非托管对话框时补配置变化关闭路径：页面根容器 onAreaChange 判断横竖翻转，或由 onConfigurationUpdate 通知页面，关闭这些浮层并保留列表等其余状态。 代码设置的视图属性也在这条路径上复位到布局初值。托管对话框对应的弹层在同一路径上改用重建后的内容与回调，不原样保留原回调；新实例 onCreate/onResume 语句的可见效果（刷新显示、复位字段、按启动 Intent 再弹窗）也在这条路径上重放。 源端重建后按新尺寸重跑的首次计算（如按容器宽度算格数）挂到 onAreaChange 的宽度变化上：首次测量照常触发，之后旧宽大于 0 且新旧宽不同才再算。

## 可选检查

- 运行中分别切换系统语言、深浅色、字号与显示大小，对照两端的画布文案、帮助文案、对话框与状态栏底色。
- 说明对话框打开时旋转，两端都只剩列表、对话框关闭。

来源支持：8 张卡 · 5 次迁移 · 5 个应用

## 来源（按需复核）

- [case-780845d2d4ab2eae2a15](../../../store/cases/case-780845d2d4ab2eae2a15/76205f7f005cef6f9308f4f10ab856a82b6a9d9342d9fd3709eab99ad0c66c5f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`76205f7f005cef6f9308f4f10ab856a82b6a9d9342d9fd3709eab99ad0c66c5f`
- [case-a95e51b69844d2f11187](../../../store/cases/case-a95e51b69844d2f11187/e42f6a772e92b6a946bc742efe37a90c306ee4b738af14df8d8becac10594761.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:5
  卡片版本：`e42f6a772e92b6a946bc742efe37a90c306ee4b738af14df8d8becac10594761`
- [case-aac91310ef7e70c88957](../../../store/cases/case-aac91310ef7e70c88957/e9dea16e5f5fff626689b42b7d8863682b54ad4e947f2648c138ea8820cee70c.json) · 结论：recommendation:6
  卡片版本：`e9dea16e5f5fff626689b42b7d8863682b54ad4e947f2648c138ea8820cee70c`
- [case-b99e7061a74e82b731f3](../../../store/cases/case-b99e7061a74e82b731f3/f12a65132c4acbc8fdba01b0f8f225d439bcb9807cf4d66d5048269d53bd1c24.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`f12a65132c4acbc8fdba01b0f8f225d439bcb9807cf4d66d5048269d53bd1c24`
- [case-d3f1bcc562a64e5f56f7](../../../store/cases/case-d3f1bcc562a64e5f56f7/5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f.json) · 结论：diagnosis, recommendation:2
  卡片版本：`5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f`
- [case-d7e5a2d2f2014ce7f39c](../../../store/cases/case-d7e5a2d2f2014ce7f39c/050e1d9c3d8b39b8081f47302db26fb62929efdf9cdf67eb98f4f7557f53685a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:5
  卡片版本：`050e1d9c3d8b39b8081f47302db26fb62929efdf9cdf67eb98f4f7557f53685a`
- [case-dd1e7cc2d529146faabb](../../../store/cases/case-dd1e7cc2d529146faabb/bb320f0bef54701d104cd64c5cf1049189471bc643fc7c70bc851fe92f24a573.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`bb320f0bef54701d104cd64c5cf1049189471bc643fc7c70bc851fe92f24a573`
- [case-f879e05d3c9a16396341](../../../store/cases/case-f879e05d3c9a16396341/69fa6f457f66c6ff881053653eea36550ebf3f4dae7c5dcc206a8258a65007ef.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`69fa6f457f66c6ff881053653eea36550ebf3f4dae7c5dcc206a8258a65007ef`
