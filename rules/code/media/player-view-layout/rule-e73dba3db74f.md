# 播放器运行时 addView 到 item 根部时，Video 放在根 Stack 最底层铺满，不放进封面区

审的是：代码
触发（任一种）：
- 读到：Fragment 或 Adapter 播放时用 addView(播放器 View, 0) 把它挂到 item 根 ConstraintLayout 的最底层，不带 XML 约束；XML 里的自定义封面/控制视图只夹在顶栏和按钮行之间；写错的样子：Video 放在顶栏和按钮行之间的 layoutWeight(1) 区里（和封面同一个 Stack），没有铺满 item；视频从标题行下方才开始
适用范围：把含运行时播放器挂载的列表项或页面（ConstraintLayout 根）转成 ArkUI 层叠布局时
做法：
- 先在 Fragment/Adapter 里查播放器的 addView / removeView / LayoutParams，再定视频层几何
- 挂到 item 根部的，写成 item 根 Stack 的第一个子组件 Video(...).width('100%').height('100%')，标题、按钮等浮层在它后面；XML 的封面区只保留封面图和按播放态的显隐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- addView(View child, int index)：index 是插入位置；子 View 没有 LayoutParams 时用该 ViewGroup 的默认参数：index 0 是最底层，不受 XML 里其他控件的约束（出处：android.view.ViewGroup#addView）
- 容器中的子元素依次入栈，后一个子元素覆盖前一个子元素：Stack 里第一个子组件在最底层，对应 addView(…, 0)（出处：arkts-layout-development-stack-layout.md，开头说明）
- Video 移到 item 根 Stack 底层 100%×100%，封面按播放态隐藏：修复后的写法，截图对照过（出处：卡里修好并验证过）
未核实：卡里的环境是 HarmonyOS 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-c85d8667f78c2cc8f53a（免费来电多多）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
