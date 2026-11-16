# 字号、字体与文字外观

源端有 TextView / EditText 的 textSize、textColor、textAppearance、fontFamily、shadow*（或没写、由主题决定），由 dp 乘文字倍率算出的字号，或 Compose MaterialTheme.typography 的命名样式、FontWeight、FontFamily(Font(R.font…))，目标端有 Text / TextInput 的 fontSize、fontColor、fontWeight、fontFamily、textShadow、registerFont 时

## 触发族

- [dp 加文字倍率得出的字号](font-size-scale/index.md)（2 条）：读到源端 textSize 由 dp 值乘文字倍率得出、行距由 dp 值得出，padding 和位置另按根尺寸比例换算；产物里 .fontSize、lineHeight、measureTextSize 或 Paragraph 的 fontSize 也乘了几何画布比例
- [TextView / EditText 的文字外观](text-appearance/index.md)（9 条）：读到 TextView / EditText 的 textColor、textSize、textAppearance、fontFamily、shadow* 属性，或这些属性没写、由主题决定；产物里 Text / TextInput 的 fontColor、fontSize、fontWeight、textShadow、height 是沿用值、近似值或 ArkUI 默认
- [Compose 文本样式的字号、字重和字体族](textstyle-font/index.md)（5 条）：读到 Compose Text 用 MaterialTheme.typography 的命名样式、FontWeight.SemiBold / Light 或 FontFamily(Font(R.font…))，产物里是 Text 的 .fontSize($r('app.float.…'))、.fontWeight(...)、.fontFamily(...) 和 registerFont
