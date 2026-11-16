# 源端靠 WebSettings 按设备宽排版时，产出给 ArkWeb 的 HTML 每条路径都注入 viewport

审的是：代码
触发（任一种）：
- 读到：源端 WebSettings 有 setUseWideViewPort(false) / setLoadWithOverviewMode(true)，清洗出的 HTML 本身没有 viewport；写错的样子：目标产出给 Web 渲染的 HTML 里，某条路径（含空文案兜底）的 <head> 没有 <meta name="viewport" …>，只有 style 注入或空的 <head></head>
适用范围：目标端自己拼装或清洗 HTML、交给 ArkWeb Web 渲染时，所有输出路径
做法：
- 每条输出路径（正常和空文案兜底）的 <head> 都写 <meta name="viewport" content="width=device-width, initial-scale=1">
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <meta name="viewport" content="width=device-width, initial-scale=1">：两条路径都注入后正文按设备宽排版（出处：卡里修好并验证过）
- setUseWideViewPort(false) 时布局宽度总是 WebView 控件的宽度（CSS 像素）：源端不靠 HTML 声明视口（出处：android.webkit.WebSettings#setUseWideViewPort）
- metaViewport(enabled: boolean): WebAttribute，默认 true；2in1 设备不解析 viewport：注入的 meta 在默认设置下会被解析（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.metaViewport）
来源：1 张卡，1 个应用
- case-60d268b503cb75aa01a2（AntennaPod）：做法第 1 步 ← 建议 4、诊断；取值 1 ← 诊断
