# 源 Activity 的 configChanges 未覆盖某项配置（只写 screenSize 时包括旋转）时，目标按源端重建时序刷新资源文案与一次性状态

ID：`lesson-94715d0df4c03a8fb5a5` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期与资源文案、一次性状态的缓存时

## 适用情境

源 Activity 在 AndroidManifest 中未声明 android:configChanges，或声明里缺 locale、uiMode、fontScale、density、orientation 等项（只写 screenSize 时旋转同样重建），实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态，或在监听器里用 setBackgroundResource 一类调用改了视图属性；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化与旋转时不重建，只回调 onConfigurationUpdate、发出 display 'change' 或改变窗口尺寸。

## 例外与边界

- 源 Activity 已在 configChanges 中声明对应项、在 onConfigurationChanged 自行处理时（ActivityInfo.configChanges：声明的项由 Activity 自行处理、不重建），按其处理代码迁移
- 边界：直接 show() 的非托管对话框在配置变化时的关闭路径见非托管对话框一条；深浅色切换中的命令式取色、系统栏与画布重解析按应用内主题切换的经验；跟随系统字号的 configuration 声明按大字体裁定的经验；SurfaceView 自建渲染线程在重建时的结果见 lesson-25731279fbe14dcecc69

## 原因

未声明 configChanges 时，除被 screenOrientation 锁定的旋转外，语言、uiMode、fontScale、densityDpi、mcc/mnc 变化都会销毁并重建 Activity；configChanges 只写 screenSize 而不含 orientation 时，旋转同样重建。旧实例先存档（onSaveInstanceState，含托管对话框状态），再销毁并关闭窗口，新实例重新构造 View、重新加载布局、重置一次性状态，再读档并按新配置重读文案、重算布局（Android SDK sources/android-36.1 的 ActivityThread.handleRelaunchActivityInner 与 Activity.performSaveInstanceState）；代码里改过、不在存档里的视图属性回到布局初值。目标 UIAbility 与页面不重建；把 onSaveInstanceState 只当作进程回收恢复，或假设切语言会触发尺寸回调，切换后仍显示旧文案与旧状态。

## 做法

1. 规格逐个 Activity 读 configChanges 与 screenOrientation，把未覆盖的配置变化（不含 orientation 时包括旋转）写成生命周期验收，并写明源端重建时序：存档（含托管对话框状态）→ 旧实例销毁、窗口关闭 → 新实例重建一次性状态 → 读档 → 按新配置重读资源、重算布局。先按运行态拆分（渲染线程在跑或已结束、对话框是否显示）再写后果；重建后消失的可见状态还包括代码里设置、未进 onSaveInstanceState 的视图属性（如点击回调里 setBackgroundResource 设的背景）。
2. 实现时在 EntryAbility.onConfigurationUpdate 比较相关字段（language、colorMode、fontSizeScale、fontWeightScale、screenDensity、mcc/mnc），显示大小变化另订阅 display.on('change') 比较密度，旋转用窗口尺寸或方向变化（页面根容器 onAreaChange 判断横竖翻转）触发，变化时显式通知页面按上述时序刷新。
3. 源 View 在构造、尺寸变化或绘制时读取的资源文案与一次性状态，在映射中标注“随配置重建刷新”，由上述通知触发，不靠尺寸回调顺带刷新。

## 可选检查

- 运行中分别切换系统语言、深浅色、字号与显示大小，对照两端的画布文案、帮助文案与状态栏底色。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-d3f1bcc562a64e5f56f7](../../../store/cases/case-d3f1bcc562a64e5f56f7/5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f.json) · 结论：recommendation:2
  卡片版本：`5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f`
- [case-f879e05d3c9a16396341](../../../store/cases/case-f879e05d3c9a16396341/69fa6f457f66c6ff881053653eea36550ebf3f4dae7c5dcc206a8258a65007ef.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`69fa6f457f66c6ff881053653eea36550ebf3f4dae7c5dcc206a8258a65007ef`
