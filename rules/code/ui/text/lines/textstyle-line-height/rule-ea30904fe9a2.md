# 文本度量公式的注释把已核和假设分开，未实测的合成规则标未验证并给必测数值

审的是：代码
触发（任一种）：
- 读到：SDK 声明对 lineSpacing 只写「Set font line spacing」，没说多行行距怎么合成；手头 dump 里没有 lineSpacing 样本；写错的样子：主题文件头注释把未实测的合成规则写成既定结论（如「natural height for one line, lineHeight pitch between lines」），没标未验证
适用范围：改主题层文本度量公式（lineHeight / lineSpacing 折算）且无法当场实测时
做法：
- 注释里分开写：有 dump 和字体度量支撑的（如单行自然高）直接写；声明没写、dump 里没样本的合成规则标「未验证假设」
- 给出下轮必测的具体数值（如某多行段落的块高和行距）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Set font line spacing.（NOTE：If the value specified is less than or equal to 0, the default value 0 is used.）：声明对 lineSpacing 的全部说明，没定义多行行距的合成（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.lineSpacing）
来源：1 张卡，1 个应用
- case-04c6d6166ebb2bcc3dfa（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
