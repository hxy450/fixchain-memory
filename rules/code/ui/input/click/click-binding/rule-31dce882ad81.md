# 可点击容器里有勾选和两行文案时，目标写成复合 Button，不用单 label 文本按钮

审的是：代码
触发（任一种）：
- 读到：布局里可点击的 LinearLayout（或带 shape 背景的容器，setOnClickListener 挂在容器上）内含 CheckBox 或图标、主文案 TextView 和小字号的次文案 TextView；写错的样子：目标写成只收一个 label 的通用文本按钮（Button(label) 一类的 builder），勾选控件和次文案都没了
适用范围：把源布局里带点击事件的复合容器（勾选或图标加多行文字）转成 ArkUI 按钮时
做法：
- 整个容器转成不带 label 的 Button()，子组件写 Column(){ Row(){ 勾选, Text(主文案) }; Text(次文案) }，容器的背景色、圆角放在 Button 上
- 写完逐个子节点对照源布局：控件类型、尺寸、文案、字号、颜色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (): ButtonAttribute：不带 label 的 Button 构造，子组件写在后面的 {} 里（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonInterface）
- (label: ResourceStr, options?: ButtonOptions): ButtonAttribute：带内置文字 label 的构造，只能显示一行文字，放不下勾选和第二行（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonInterface）
- Button 可以包含单个子组件：多个子节点要先包进一个 Column 或 Row（出处：ts-basic-components-button.md，子组件）
- Button 内 Column{ Row{ 14vp 勾选图标 + 主文案 }, Text(Span…) 次文案 } 替换单 label 按钮后与源布局一致：修好后的结构（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a3404675917f8a352eb9（话费流量查询助手）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断
