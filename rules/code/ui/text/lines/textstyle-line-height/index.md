# Compose TextStyle 的 lineHeight

agent 会看到什么：读到 Compose TextStyle（多在 Typography 里）带 fontSize / lineHeight、没设 lineHeightStyle，产物里是 Text 的 .lineHeight()、.lineSpacing()、主题文件里的行高派生值，或按 lineHeight 常量算出的容器高度

## 规矩

- rule-c67260e64b9a｜TextStyle 行高迁成 lineSpacing(lineHeight − fontSize)，只加在行间｜读到：Compose `TextStyle(fontSize = …, lineHeight = …)`，没设 `lineHeightStyle`；写错：Text 上（或 AttributeModifier<TextAttribute> 的 applyNormalAttribute 里对所有 Text）写了 .lineHeight(…)
- rule-c03ed1509647｜Compose TextStyle 带 lineHeight 的单行文本，Text 不写 .lineHeight()｜读到：Compose `TextStyle(fontSize = …, lineHeight = …)` 没有设 `lineHeightStyle`，用在单行文本（标题、价格、按钮文字等）上；写错：对应的 ArkUI `Text` 上写了 `.lineHeight(…)`，值取样式行高（常量、`$r('app.float.…')` 或主题表字段）
- rule-61a3e7b3063f｜按文本高度给容器定高时，单行文本取字体自然高度，不用样式 lineHeight｜读到：Compose 里行按内容包裹（LazyRow / Column 无固定高度），其中 Text(style = …titleMedium) 带 lineHeight；写错：ArkUI 横向 List 的交叉轴高度写成字面常量（const …_HEIGHT: number = <数>），注释按「某令牌 lineHeight N」算文本盒高
- rule-7741ca63745f｜转写 Typography 常量表时，同时给出单行自然高度和多行行距两个派生值｜读到：Compose `Typography` 里各 `TextStyle` 的 `fontSize` / `lineHeight`，未设 `lineHeightStyle`；写错：目标主题文件里的 TextStyle 常量只有 `lineHeight` 字段，没有单行自然高度、行间距派生值，也没注释说明不能原样传给 `.lineHeight()`
- rule-ef4b658d819d｜不能当场重编实测时，改单行行高的方案不动多行已正确的 lineHeight 路径｜读到：派工写明「不重编、不复测」；源端同一 TextStyle 的 lineHeight 同时用于单行和多行；写错：把主题层所有 Text 的 .lineHeight 整体换成按未验证公式算的 .lineSpacing，连多行本已正确的段落一起改
- rule-ea30904fe9a2｜文本度量公式的注释把已核和假设分开，未实测的合成规则标未验证并给必测数值｜读到：SDK 声明对 lineSpacing 只写「Set font line spacing」，没说多行行距怎么合成；手头 dump 里没有 lineSpacing 样本；写错：主题文件头注释把未实测的合成规则写成既定结论（如「natural height for one line, lineHeight pitch between lines」），没标未验证
