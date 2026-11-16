# 源输入框用 visualTransformation 高亮链接时，目标用 RichEditor 加 span 样式

审的是：代码
触发（任一种）：
- 读到：`OutlinedTextField(visualTransformation = { TransformedText(…AnnotatedString…, OffsetMapping.Identity) })`，按 URL 加链接色；写错的样子：目标描述框是纯文本 `TextArea`，编辑态没有链接高亮，登记了 UNC 一类的不确定占位
适用范围：源端可编辑输入框在编辑态显示富文本样式（链接高亮）时
做法：
- 用 RichEditor({ controller }) 承载输入，文本变化后按 URL 范围用 controller.updateSpanStyle({ start, end, textStyle: { fontColor: 链接色 } }) 着色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- updateSpanStyle(value: RichEditorUpdateTextSpanStyleOptions | RichEditorUpdateImageSpanStyleOptions | RichEditorUpdateSymbolSpanStyleOptions): void：按范围改 span 样式（出处：鸿蒙 SDK 的 ets/component/rich_editor.d.ts，RichEditorBaseController.updateSpanStyle）
- addTextSpan(content: ResourceStr, options?: RichEditorTextSpanOptions): number（@since 20）：插入带样式的文本段（出处：鸿蒙 SDK 的 ets/component/rich_editor.d.ts，RichEditorController.addTextSpan）
- 描述框改用 RichEditor 承载 URL 高亮后编辑态有链接色：卡里的修法（出处：卡里修好并验证过）
未核实：卡里没写 span 样式的具体调用；updateSpanStyle 的选项按声明写
来源：1 张卡，1 个应用
- case-3b8b620c1c7fa2848a34（Cofi）：做法第 1 步 ← 诊断、建议 5；取值 3 ← 诊断
