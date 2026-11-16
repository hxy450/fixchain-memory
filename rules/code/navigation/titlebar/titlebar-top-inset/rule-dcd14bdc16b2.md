# 自绘顶栏不在同一容器上同时写 height(N) 和 padding(top: inset)，分两层或高度加 inset

审的是：代码
触发（任一种）：
- 读到：源端顶栏用 TopAppBar 加 statusBars insets 避让，内容高度固定；写错的样子：同一个 Row 上写 .height(64).padding({ top: windowTopPadding })，菜单却按 windowTopPadding + 64 定位
适用范围：全屏窗口下自绘的固定高度顶栏
做法：
- 把状态栏避让和顶栏内容高度分两层：外层 Column().padding({ top: inset })，内层 Row().height(N)；或单层写 .height(N + inset)
- 套用模板或已有页面的顶栏写法前，先核对它是否把 padding 放进了固定 height
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 设置了固定 width 和 height 时，组件内容大小 = width、height 减去 padding 和 border：padding 计入 height，height(N) 加 padding(top: inset) 会把内容区压成 N - inset（出处：arkts-layout-development-overview.md，布局元素的组成）
- height(value: Length) 与 padding 的单位都是 vp：inset 与 N 同单位相加（出处：ts-universal-attributes-size.md，height、padding）
- 外层 padding(top = inset)、内层固定高度：修复后的顶栏盒模型（出处：卡里修好并验证过）
针对本应用要查的：
- 源端顶栏内容高度 N：源工程顶栏所用的 TopAppBar 组件或布局里给出的高度；读出 dp 值，按 vp 写进内层 height
来源：1 张卡，1 个应用
- case-b3c176b95cabcc03a434（jerboa）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 3 ← 诊断
