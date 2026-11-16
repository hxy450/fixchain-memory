# 源 Activity 未声明 configChanges 的 Compose 界面，规格写“重建后按新尺寸重算”验收

审的是：规格
触发（任一种）：
- 读到：AndroidManifest 里 Activity 没有 android:configChanges；Compose 组件在 BoxWithConstraints 里读 maxWidth，再在带键的 LaunchedEffect(key)（键不含宽度）里按宽度算格数、列数写回 ViewModel；写错的样子：AC 写“仅 key 变化触发、画布宽度变化不重算”或“转屏后两端均不重算”，同一份规格里又写着源端转屏重建、remember 复位
适用范围：规格提取阶段，源端是 Compose、承载它的 Activity 未声明 configChanges、首次组合副作用读取容器尺寸时
做法：
- 把“重建后按新尺寸重算”单独写成一条验收：转屏或窗口尺寸变化时整棵组合重新进入，带键的 LaunchedEffect、remember(key) 不论键变没变都按新约束再跑一次；判据给出转屏前后两个宽度下的期望值
- 不写“宽度变化不重算”“键不变就不重跑”：后者只描述同一组合内的重组
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- configChanges 没有列出的配置变化发生时，Activity 会被重启：未声明 configChanges 时转屏走重建，不是重组（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges（按应用的 compileSdk 取对应平台）；android.content.pm.ActivityInfo#configChanges）
- 转屏涉及 orientation（用户旋转设备）和 screenSize（横竖切换时可用尺寸变化）两个标志：configChanges 里两者都声明了才不重建（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 orientation、screenSize（按应用的 compileSdk 取对应平台））
- 源端转屏重建后首次组合，LaunchedEffect 再跑一次并读到新的 maxWidth，按新宽度重算格数：源端可观察行为是“转屏后重算”（出处：卡里修好并验证过）
针对本应用要查的：
- 源 Activity 转屏时是否重建：源工程 AndroidManifest.xml 里承载该 Compose 界面的 activity 元素的 android:configChanges；没写，或没同时含 orientation 和 screenSize 时，转屏会重建、整棵组合重新进入
未核实：Compose 带键 LaunchedEffect 在重建后随首次组合重跑，出自卡里上机观察，本机没有 Compose 运行时源码核对
来源：1 张卡，1 个应用
- case-d7e5a2d2f2014ce7f39c（GameOfLife）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
