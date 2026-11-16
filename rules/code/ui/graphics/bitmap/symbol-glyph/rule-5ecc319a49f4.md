# TextView 文字加减号当按钮时按原字形画，不用带圆圈的近似 symbol

审的是：代码
触发（任一种）：
- 读到：粗体 TextView 的 android:text 就是“-”“+”，充当步进器的减、加按钮（截图里是无圆环的普通字符）；写错的样子：写成 SymbolGlyph($r('sys.symbol.minus_circle')) 之类外形不同的 symbol，减号多了圆环，与加号不对称
适用范围：源端用 TextView 字符充当按钮、目标图标库里没有同形 symbol 时
做法：
- 减号用形状画出同形短横：Divider().width(<短横长>).strokeWidth(<粗细>).color(<源端文字色>)（或 Rect、工程已有资源）；加号用 sys.symbol.plus 并 .fontWeight(FontWeight.Bold) 对上源端粗体
- 技能里“只用已验证的 symbol 名称”约束的是名称合法，不是允许改外形；没有同形名称时不拿外形不同的近似 symbol 顶替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- strokeWidth(value: number | string): DividerAttribute：水平 Divider 的 strokeWidth 控制线的高度（即短横粗细），不支持百分比（出处：鸿蒙 SDK 的 ets/component/divider.d.ts，DividerAttribute.strokeWidth；ts-basic-components-divider.md，strokeWidth）
- fontWeight(value: number | FontWeight | string): SymbolGlyphAttribute：给 symbol 加粗，对应源端 textStyle=bold（出处：鸿蒙 SDK 的 ets/component/symbolglyph.d.ts，SymbolGlyphAttribute.fontWeight）
- 减号改为 Divider 短横、加号改为加粗的 sys.symbol.plus 后，外形与源端一致：形状画法同样满足技能对图标的约束（出处：卡里修好并验证过）
针对本应用要查的：
- 短横的长度、粗细和颜色：源工程布局 XML 里这个 TextView 的 android:textSize、android:textStyle、android:textColor，以及安卓截图；按字号估出减号横线的长和粗，颜色取 textColor，让减号与加号的笔画粗细一致
来源：1 张卡，1 个应用
- case-6ba16d2344b52f8fca51（刺猬猫阅读）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
