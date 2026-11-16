# 决定纵向排布的单行 Text 按源端行框显式写 height，列表行高取各行之和

审的是：代码
触发（任一种）：
- 读到：wrap_content 单行 TextView（textAppearance 或 sp 字号，includeFontPadding 取默认）是标题、列表项两行文字或页脚；写错的样子：对应 Text 只有 .fontSize(...)，没有 .height(...)，标题、列表行比源端矮
适用范围：单行文字的高度决定下方分隔线、列表行高或按钮行位置时
做法：
- 给这些 Text 写 .height(<源端行框 dp>)：字号 × 约 1.33–1.39（Roboto + includeFontPadding）；两行文字组成的列表行，行高等于两段行框之和
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- height(value: Length): T，单位 vp，缺省时用内容需要的高度：显式高度覆盖鸿蒙字体度量算出的默认高度（出处：ts-universal-attributes-size.md，height）
- 不写 height 时 textAppearanceLarge（22sp）标题在鸿蒙端约 25.7vp、源端 29.71dp；各单行 Text 按源端行框显式写 height 后与源端对齐：鸿蒙默认 Text 比安卓默认行框矮（出处：卡里修好并验证过）
针对本应用要查的：
- 每行文字的源端行框高度：源工程布局 XML 里该 TextView 的 android:textSize 或 textAppearance（平台 data/res/values/styles.xml 的 TextAppearance.* 给出字号）；sp 数乘约 1.33–1.39 得 dp；有实测 bounds 时以实测为准
未核实：比例来自 Roboto 在卡里设备上的实测，其他字体、字体缩放下没核
来源：1 张卡，1 个应用
- case-c3ff122a5abfda1fa55d（Blockinger）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断
