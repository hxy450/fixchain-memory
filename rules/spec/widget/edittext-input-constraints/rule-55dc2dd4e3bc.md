# 可编辑又分段着色的 EditText，规格映射到 RichEditor，不写 TextArea 加 Span

审的是：规格
触发（任一种）：
- 读到：源码里同一个 EditText（含 AppCompatEditText）常驻可编辑，又以 setText(text, BufferType.SPANNABLE) 放入分段着色的 Spannable；写错的样子：规格的转换决策写「TextArea + 着色用分段 Span 还原」这类组件不支持的组合，或写成只读 Text 与编辑框切换
适用范围：规格提取时，为既要编辑又要分段样式的源控件选目标组件
做法：
- 转换决策写成「RichEditor({ controller })，按段 controller.addTextSpan(段文本, { style: { fontColor: 段颜色 } })」，写入前核对所选组件是否支持子 Span 或样式片段
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextArea 子组件：无：TextArea 不能承载 Span（出处：ts-basic-components-textarea.md，子组件）
- RichEditor：支持图文混排和文本交互式编辑的组件：可编辑又能分段设样式（出处：ts-basic-components-richeditor.md，RichEditor）
- addTextSpan(content: ResourceStr, options?: RichEditorTextSpanOptions): number：按段加文本，options.style.fontColor 定这段的颜色，options.offset 定插入位置（出处：鸿蒙 SDK 的 ets/component/rich_editor.d.ts，RichEditorController.addTextSpan、RichEditorTextSpanOptions）
未核实：卡里环境是 API 24，按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-4a5592fd88f74b1c16a4（MifareClassicTool）：做法第 1 步 ← 建议 1
