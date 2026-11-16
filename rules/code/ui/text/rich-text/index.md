# 富文本、链接与标记

源端有 SpannableString.setSpan、ForegroundColorSpan、ClickableSpan / URLSpan、LinkMovementMethod、Linkify.addLinks、Html.fromHtml、Compose buildAnnotatedString / LinkAnnotation，或用 react-markdown 渲染 Markdown，目标端有 Span、RichEditor、TextController、Text 上的手势和自写的链接或标记解析时

## 触发族

- [带 LinkAnnotation 链接的 AnnotatedString 文本](annotated-string-links/index.md)（4 条）：读到 Compose 文本或输入框经 buildAnnotatedString、LinkAnnotation、visualTransformation 给 URL 加链接；交回的是直接显示原始字符串的 Text 或纯文本 TextArea，链接不着色也不可点
- [Html.fromHtml 生成的文字内容](html-fromhtml-text/index.md)（2 条）：读到源端用 Html.fromHtml / HtmlCompat.fromHtml 给 TextView 或对话框设文本（带 <b>、<a> 的串，或 &#8226; 这类单个字形当圆点），产物里是 Text(...) 直接显示或 Text('•') 拼出来的写法
- [Spannable 分段着色的文字](spannable-color/index.md)（2 条）：读过的源码里用 SpannableString.setSpan(ForegroundColorSpan, start, end, …) 或 Spannable 文本给一段字着色（含可编辑的 EditText）；交回的代码里拆出的 Span 区间、RichEditor 还是 Text / TextArea
- [Linkify 自动链接的识别和切分](linkify-autolink/index.md)（2 条）：读到源端 Linkify.addLinks、LinkifyPlugin.create(Linkify.WEB_URLS) 在文本上跑一个或多个 Pattern、按 getSpanStart / getSpanEnd 原位挂 URLSpan；产物里自动链接的正则只认 https?:// 或 www. 前缀，或切 run 时命中段和间隔文本的输出顺序被打乱
- [TextView 里按触点命中的链接 span（ClickableSpan、LinkMovementMethod）](link-span-touch/index.md)（1 条）：读到源端用 BetterLinkMovementMethod / LinkMovementMethod 按触点找 ClickableSpan、URLSpan，在按下的那个 span 上派发点击或长按；产物里 Text 上挂组件级 LongPressGesture，回调取第一个链接，没有经 TextController 的 getLayoutManager 按坐标找字符
- [Markdown 渲染和自写的行内标记解析](markdown-inline-parse/index.md)（1 条）：读到源端用 react-markdown / remark-gfm 这类库渲染 Markdown、规格要求不成对的标记按字面输出；产物里自写的行内解析按 indexOf('**') / indexOf('*') 分支产出粗体、斜体 Span
