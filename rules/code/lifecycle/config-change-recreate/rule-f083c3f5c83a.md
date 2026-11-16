# 源端旋转会重建且视图状态由代码设置时，目标在方向变化时把它复位到初值

审的是：代码
触发（任一种）：
- 读到：AndroidManifest 的 android:configChanges 不含 orientation；点击监听里 setBackgroundResource(...) 改视图，没存进 onSaveInstanceState；写错的样子：目标把它写成页内 @State，旋转后保持不变
适用范围：源 Activity 旋转会重建、目标页面旋转不重建时，代码设置的可见状态
做法：
- 监听窗口方向变化（如 display.on('change') 里比较 rotation），方向变了就把这类状态复位到布局初值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 监听窗口区方向变化、清掉代码设置的状态后，与源端旋转后复位一致：修复后的写法（出处：卡里修好并验证过）
- configChanges 未列出的配置变化发生时 Activity 重启；orientation = 0x0080：源端旋转即重建（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-d3f1bcc562a64e5f56f7（Bubble Shooter）：做法第 1 步 ← 建议 4、诊断；取值 1 ← 诊断
