# Activity 未声明 configChanges 时，规格写明配置变化重建的 AC 和时序

审的是：规格
触发（任一种）：
- 读到：AndroidManifest.xml 里该 Activity 没有 android:configChanges（可能只有 android:screenOrientation），Activity 实现了 onSaveInstanceState，并在 onCreate 里按 savedInstanceState 恢复；写错的样子：规格的实现映射把 onSaveInstanceState / savedInstanceState 分支写成「进程恢复」「不迁移，冷启即 load」，生命周期 AC 只覆盖页面显隐和杀进程冷启，没有配置变化重建
适用范围：规格提取阶段，把安卓 Activity 生命周期回调和清单属性映射成目标端生命周期契约时
做法：
- 生命周期 AC 里写明：语言、深浅色、字号、字重、显示大小、mcc/mnc 变化时源端销毁重建 Activity；screenOrientation 固定只排除旋转这一项
- 写明重建时序：save → 新 View 构造并重置一次性状态 → load → 重读资源文案、重算布局；对话框随旧窗口关闭
- 目标映射写明触发入口：UIAbility.onConfigurationUpdate 比较相关配置字段，显示大小变化另用 display.on('change') 比较 densityPixels
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- configChanges 没写的配置项一变化，Activity 就会被重启；写了的才留在运行中并回调 onConfigurationChanged：未声明 configChanges 时 savedInstanceState 分支在配置变化重建时也会走（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges（按应用的 compileSdk 取对应平台））
- locale、uiMode、fontScale、fontWeightAdjustment、density、mcc、mnc、orientation：configChanges 里对应语言、深浅色、字号、字重、显示大小、SIM 国家码和网络码、旋转的取值名（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的各 flag（按应用的 compileSdk 取对应平台））
- mcc、mnc：从 Android O 起默认不因它们重建 Activity，要重建需在 recreateOnConfigChanges 里声明：写 mcc/mnc 重建前按应用的清单核对（与卡里的说法有出入，见冲突）（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 mcc、mnc（按应用的 compileSdk 取对应平台））
- UIAbility.onConfigurationUpdate() 里拿到最新的环境变量信息，无需重启 UIAbility：目标端配置变化不重建，规格要另写刷新入口（出处：subscribe-system-environment-variable-changes.md，在UIAbility组件中订阅回调）
- 切换系统语言后源端重建并显示新语言，目标端不重建，画布、帮助文案和确认框都保持旧状态：不写进规格时的实际后果（出处：卡里修好并验证过）
针对本应用要查的：
- 这个 Activity 自己处理哪些配置变化：源工程 AndroidManifest.xml 里该 <activity> 的 android:configChanges、android:screenOrientation 和 android:recreateOnConfigChanges；列出的项不重建；没列的配置项都按重建写进 AC；screenOrientation 固定的去掉旋转
来源：1 张卡，1 个应用
- case-f879e05d3c9a16396341（2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2；取值 5 ← 诊断
