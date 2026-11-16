# dp 加文字倍率得出的字号

agent 会看到什么：读到源端 textSize 由 dp 值乘文字倍率得出、行距由 dp 值得出，padding 和位置另按根尺寸比例换算；产物里 .fontSize、lineHeight、measureTextSize 或 Paragraph 的 fontSize 也乘了几何画布比例

## 规矩

- rule-45eaf345e152｜源端字号只由 dp 和文字倍率得出时，目标 fontSize、lineHeight 不乘几何画布比例｜读到：源端文本的 textSize 由 dp 值乘文字倍率得到、行距 spacingAdd 由 dp 值得到；padding、背景、位置另按根尺寸与设计宽度之比换算；写错：目标写了一个按「渲染宽度 / 设计宽度」缩放的通用换算函数，并对 .fontSize(...)、minFontSize、maxFontSize、lineHeight 一并调用
- rule-523e9b9602d9｜新增文本测量或 Paragraph 绘制时，字号按源端 dp 公式乘 vp2px(1)，几何比例单独传｜读到：源端文本的 textSize 由 dp 值乘文字倍率得到，不含根尺寸或设计宽度比例；写错：新增的 measureTextSize 或 text.TextStyle 的 fontSize 照搬了已有组件里乘画布比例的表达式，或写成 fontSize * vp2px(画布比例)
