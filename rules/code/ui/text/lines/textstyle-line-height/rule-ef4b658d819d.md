# 不能当场重编实测时，改单行行高的方案不动多行已正确的 lineHeight 路径

审的是：代码
触发（任一种）：
- 读到：派工写明「不重编、不复测」；源端同一 TextStyle 的 lineHeight 同时用于单行和多行；写错的样子：把主题层所有 Text 的 .lineHeight 整体换成按未验证公式算的 .lineSpacing，连多行本已正确的段落一起改
适用范围：修单行文本被 lineHeight 撑高、又不能当场重编实测时
做法：
- 只对单行文本去掉 .lineHeight，多行段落保留 .lineHeight；或运行期用 MeasureUtils 实测后再算 spacing
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- measureTextSize(options: MeasureOptions): SizeOptions：MeasureUtils 运行期测文本宽高，实例由 UIContext.getMeasureUtils() 取得（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- .lineHeight 路径下多行段落块高 = 行数 × 行高，多行是对的；单行文本盒被撑到行高：lineHeight 路径的已知表现（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-04c6d6166ebb2bcc3dfa（Jetsnack）：做法第 1 步 ← 建议 3；取值 2 ← 诊断
