# 动态布局文本的字号、行距按源端 dp × 文字倍率落成 vp，只有 bounds、padding、背景等几何乘设计画布比例

## 何时使用

动态或灵活组件的渲染实现阶段，源端字号按 dp 乘应用自己的文字倍率计算、几何另按画布比例缩放，把这类动态布局文本的字号、行距换算成 ArkUI 预览、测量或原生绘制尺寸时

## 适用情境

源端动态文本以 fontSize.dpF × dynamicTextScale × fontSizeScale 设字号、以 lineSpacing.dpF 设行距，只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用 renderWidth / document.width 一类画布比例统一换算几何。

## 例外与边界

- “落成 vp”要带单位写：Text、TextInput 的 fontSize，Text 的 lineHeight、minFontSize、maxFontSize 传纯数字时按 fp 解释，会再随系统字体大小设置变化，要按 vp 落值须传带单位的字符串（如 `${v}vp`）；@ohos.graphics.text 的 TextStyle.fontSize（Paragraph 排版）单位是 px，用 vp2px 换算；文本测量的 MeasureOptions.fontSize 传纯数字时 API 12 起按 fp、之前按 vp，同样用带单位的字符串指明。
- 源端的文字倍率（如动态文字缩放、字号缩放）不等于 1 时照乘，不因为“不乘画布比例”把它们一起去掉。

## 原因

写出通用的 scaled() 后对所有数值一律调用，会把几何画布比例套到字号与行距上，画布比例小于 1 时文字整体变小；新增的测量或原生绘制路径照搬现有表达式，偏差随之扩散。

## 做法

1. 逐属性核对源端单位与缩放链：字号、行距、最小与最大字号按源端公式落为 vp，只有几何属性乘画布比例；新增 measureText、Paragraph 等路径时从源端公式重新推导字号，几何比例作为单独参数传入，px 换算只用 vp2px(1)。

## 可选检查

- 加一条回归：画布比例不为 1 时，字号仍等于源端 dp 值，几何仍按比例缩放。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕vp 按屏幕像素密度换算；fp 也按密度换算，但另外随系统字体大小设置变化；数值不带单位时默认按 vp
- 〔做法第 1 步〕Text、TextInput 的 fontSize 传 number 时按 fp 解释；应用没有另设 fontSize 时默认 16fp（穿戴设备另有默认值）
- 〔做法第 1 步〕Text 的 minFontSize、maxFontSize 单位是 fp，字符串可带单位（如 "10fp"）；要和 maxFontSize、maxLines 一起设置才生效
- 〔做法第 1 步〕Text 的 lineHeight 传 number 时单位是 fp，字符串可带单位；设置值不大于 0 时不限制行高，由系统按字号自适应
- 〔做法第 1 步〕@ohos.graphics.text 的 TextStyle.fontSize（Paragraph 排版用）单位是 px，没写时默认 14.0
- 〔做法第 1 步〕文本测量的 MeasureOptions.fontSize 为 number 时从 API 12 开始按 fp，API 12 之前按 vp；没写时默认 16
