# 只响应点击长按的 ImageButton 转成 Image 时，每个 Image 写 .draggable(false)

审的是：代码
触发（任一种）：
- 读到：ImageButton，或挂了 setOnClickListener / setOnLongClickListener 的 ImageView（快门、图库缩略、屏上图标等），源端没有任何拖放逻辑；写错的样子：Image(...) 直接挂 .onClick，或放在挂 onClick / LongPressGesture 的 Stack、Button 里，修饰链上没有 .draggable(false)
适用范围：源端没有拖放、目标用 ArkUI Image 承载点击或长按控件时（Image 默认可拖拽自 API 10 起，出自文档）
不适用的情形：SymbolGlyph 图标和 Canvas 绘制的图形不需要
做法：
- 每个承载点击或长按的 Image 上写 .draggable(false)；父 Stack 或 Button 挂 onClick 时也不能省，父容器的点击、长按和命中设置保留
- 输出前在按钮、图标相关的 Builder 和组件里逐个找 Image(，核对修饰链都有 .draggable(false)；默认值按 Image 自己的声明定，不套通用属性的默认值或安卓同名控件的行为
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- draggable(value: boolean): ImageAttribute，默认 true：Image 自己的拖拽开关，默认可拖拽（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.draggable）
- API 9 及之前默认 false，API 10 及之后默认 true；为 true 时绑定的长按手势不生效，要用自定义手势须设为 false：不关掉拖拽时 LongPressGesture 不触发、按住进入拖拽预览（出处：ts-basic-components-image.md，draggable）
- draggable(value: boolean): T，默认 false：通用属性的默认值，和 Image 不同（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.draggable）
- draggable(value: boolean): TextAttribute，默认 false：同族接口：Text 的拖拽开关，要配合 copyOption 使用（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.draggable）
- 默认支持拖出的组件：Search、TextInput、TextArea、RichEditor、Text、Image、Hyperlink：这些组件用 draggable 控制默认拖拽（出处：ts-universal-events-drag-drop.md，页首说明）
- 6 处承载点击的 Image 加 .draggable(false) 后，点按不再进入拖拽预览，点击能正常触发：修好后的写法（出处：卡里修好并验证过）
未核实：image.d.ts 里写默认 true 的注释块标 @since 11（@since 9 的块写 false），文档写 API 10 起为 true
来源：1 张卡，1 个应用
- case-1071843a480186d94d42（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、建议 3；例外 1 ← 建议 2；取值 6 ← 诊断
