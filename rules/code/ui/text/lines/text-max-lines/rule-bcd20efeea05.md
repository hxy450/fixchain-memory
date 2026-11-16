# 源控件是第三方 TextView 子类且无 ellipsize 时，先查库的截断策略，逐行回退省略要自排版

审的是：代码
触发（任一种）：
- 读到：布局 xmlns 声明了库命名空间，控件是库的 TextView 子类（如 com.neopixl.pixlui.components.textview.TextView），带 android:singleLine 或 android:maxLines，没有 android:ellipsize；写错的样子：目标一律写 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })`，多行正文收起时没有「…」或长标题在词中截断
适用范围：源控件的截断由第三方库决定，且库在多行末尾按空格回退后加「…」时
做法：
- 先确认库自身的截断策略；是逐行按空格回退加「…」的，用 @ohos.graphics.text 自排版：new text.ParagraphBuilder(paragraphStyle, fontCollection) 以与 Text 相同的字体字号 addText、build() 后 layoutSync(宽度 px)
- 用 getLineCount() 和 getActualTextRange(i, false) 取前 N 行，在第 N 行按空格回退到能放下「…」处、去掉尾部标点再加「…」，把结果交给 Text 显示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(paragraphStyle: ParagraphStyle, fontCollection: FontCollection)：ParagraphBuilder 的构造（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.text.d.ts，ParagraphBuilder.constructor）
- layoutSync(width: number): void，width 单位 px：按单行最大宽度排版（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.text.d.ts，Paragraph.layoutSync）
- getLineCount(): number；getActualTextRange(lineNumber: number, includeSpaces: boolean): Range：取行数和每行实际显示的文本范围（行号从 0 起）（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.text.d.ts，Paragraph.getLineCount、Paragraph.getActualTextRange）
- 用 Paragraph 以同字体同宽取行的自排版替换 maxLines+Ellipsis 后，收起视图正文有「…」、标题不再词中截断：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 库控件的截断策略：依赖库源码里这个 TextView 子类（看是否覆盖 setEllipsize、onDraw 或 setText 里截断文本）；读出它取几行、回退规则和尾部处理，照写自排版逻辑
未核实：卡的环境是 API 24，本机按 API 23 核实；layoutSync、getActualTextRange 的当前声明标 @since 22
来源：1 张卡，1 个应用
- case-a767fbce6dbdeb152c90（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
