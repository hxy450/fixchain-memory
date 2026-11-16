# 以对话框库为锚点封装对话框时，把库 Builder 的行距倍数缺省落成正文 lineSpacing

审的是：代码
触发（任一种）：
- 读到：源端用 material-dialogs 等对话框库的 Builder 构造对话框（库内对正文 setLineSpacing(0, 1.2) 这类缺省不在源码树里）；写错的样子：目标对话框正文 Text 只有 fontSize / fontColor，没有 .lineSpacing(…)，注释却声称对齐库的布局语义
适用范围：以第三方对话框库为锚点用 @CustomDialog 等封装对话框时
做法：
- 把库 Builder 的缺省值（如 contentLineSpacingMultiplier = 1.2）写进组件注释，并落成正文 .lineSpacing(LengthMetrics.vp(1.2 × 单行自然行高 − 字号))，不只复刻内边距与字号
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- lineSpacing(value: LengthMetrics): TextAttribute，默认 0，≤0 时取 0：Text 的行间距（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.lineSpacing）
- static vp(value: number): LengthMetrics；static px(value: number): LengthMetrics：构造 lineSpacing 参数（出处：鸿蒙 SDK 的 ets/api/arkui/Graphics.d.ts，LengthMetrics.vp、LengthMetrics.px）
- setLineSpacing(add, mult)：除最后一行外每行高度乘 mult 再加 add（add 单位 px）：源端行距倍数的含义（出处：android.widget.TextView#setLineSpacing）
- lineSpacing(value: LengthMetrics): TextAreaAttribute：同族接口：TextArea 的行间距（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.lineSpacing）
- 正文加 lineSpacing = 1.2×单行自然行高 − 字号 后与源端一致：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 库 Builder 的正文排版缺省：依赖库源码里对话框 Builder 的字段缺省值和初始化正文的那段（如 content.setLineSpacing(…)），按应用依赖的版本；读出行距倍数、额外行距等，写进组件注释并换算成 lineSpacing
未核实：公式 1.2×单行自然行高 − 字号 与 Android「每行高度乘 mult」的换算关系没有逐项核实，出自卡里的修法
来源：1 张卡，1 个应用
- case-a767fbce6dbdeb152c90（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；取值 5 ← 诊断
