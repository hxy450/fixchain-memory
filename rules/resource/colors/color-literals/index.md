# 源端写明的颜色值转 color.json

agent 会看到什么：源端自己写明了颜色：colors.xml 与 values-night、布局里的字面色值、Compose 的 Color(0x…) 和深浅两套、数据源里的色值；color.json 里原样写了 @color / ?attr 引用，字节序或值和源不一致，dark 从 base 派生，漏了某个色、改了共享 token，或追加了按截图估的色

## 规矩

- rule-4e0948126e42｜colors.xml 转 color.json 时值只能是十六进制或已定义的 $color:name，不原样写引用｜读到：colors.xml 的 <color> 值是 @android:color/…、指向本次没转换资源的 @color/name，或 ?attr/…；写错：color.json 里出现 "value": "@android:color/black"、"@color/…"、"?attr/…"，或 $color:name 指向文件里没有的条目
- rule-66529d3b89cf｜源色值没有等值资源时，color.json 追加专属键，不改共享 token 的值｜读到：源布局元素的 android:textColor 等写了字面色值，工程颜色 json 里同前缀、同色系 token 的 value 与它不同；写错：color.json 里没有 value 等于源色值的项（同一批其他颜色都按源值建了键，唯独漏了这一个），或把被其他页面共享的 token 的 value 改成了本页色值
- rule-df75a0f0b571｜选项色值和素材按源数据源迁入资源，不在 color.json 里追加按截图估的色｜读到：源 ViewModel 数据源里列出颜色值（含渐变两端）和 R.drawable 位图素材；写错：目标 resources/base/element/color.json 里追加了源数据源里没有、按截图估的色值；边框等位图素材没有迁进 resources/base/media
- rule-4d887090bf41｜colors.xml 的 8 位色 #AARRGGBB 原样写进 color.json，不重排成 #RRGGBBAA｜读到：源 res/values*/colors.xml 里有 8 位带透明度的 <color>（#AARRGGBB，前两位是透明度，如 #80000000）；写错：目标 element/color.json 里同名键的值首两位和末两位互换（成了 #RRGGBBAA），或转换脚本把 a、r、g、b 拆开后按 {r}{g}{b}{a} 输出
- rule-8249884d8248｜深色 color.json 的值从浅色结果派生时，逐项对照安卓深色源值｜读到：源 res/values-night*/colors.xml（或同义的 *_dark / *_light 颜色对）给出深色值；写错：目标 dark/element/color.json 的值是从 base 的 color.json 转换结果复制或派生来的（如把 *_dark 复制成 *_light），和安卓同名源值不一致
- rule-afe1116fb5a3｜给主题色追加 base 颜色键时，同时按深色套写 dark 的同名键，已有文件只追加不覆盖｜读到：源端 Compose 主题按 isSystemInDarkTheme() 在 Light / Dark 两套颜色里选，深色套里同名颜色取不同值；写错：base/element/color.json 追加了主题色键，dark/element/color.json 里没有同名键
- rule-51e49bf19156｜源端渐变用到的调色板色阶在 color.json 缺条目时，按调色板名补上同值条目｜读到：源端主题里 val 名字 = Color(0xAARRGGBB) 定义了渐变用到的色阶，组件经 Brush 用它们着色；写错：color.json 里没有这些色阶的 name 或同值条目（只补了别的条目），代码改用了值不同的已有条目
