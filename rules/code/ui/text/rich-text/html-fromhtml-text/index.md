# Html.fromHtml 生成的文字内容

agent 会看到什么：读到源端用 Html.fromHtml / HtmlCompat.fromHtml 给 TextView 或对话框设文本（带 <b>、<a> 的串，或 &#8226; 这类单个字形当圆点），产物里是 Text(...) 直接显示或 Text('•') 拼出来的写法

## 规矩

- rule-7cd8b2fdef72｜带样式文案用公共富文本组件解析成 Span、链接 Span 设 onClick，不用 Text($r(...)) 直出｜读到：源端用 HtmlCompat.fromHtml / Html.fromHtml、setMessage(resId) 或 android:text 显示带 <b>/<a> 的串，并 setMovementMethod(LinkMovementMethod.getInstance())；写错：鸿蒙端对话框正文写 Text($r('app.string.…')) 或 Text(...) 直接显示，CDATA 文案露出标签原文、链接不可点；或正文链接 Span 只着色不响应点击，另在正文下加一行外链
- rule-4a7a8a6e055e｜源端单个字形当指示器时，目标按几何用 Circle 画；要用 Text 先量步进和位置｜读到：源码在循环里 new TextView + setText(Html.fromHtml("&#8226;")) + setTextSize(大字号)，逐个 addView 作页码点；写错：Row 里 ForEach 出 Text('•').fontSize(字号)，只靠字号对齐，没按源端步进、直径、垂直位置绘制
