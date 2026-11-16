# 带样式文案用公共富文本组件解析成 Span、链接 Span 设 onClick，不用 Text($r(...)) 直出

审的是：代码
触发（任一种）：
- 读到：源端用 HtmlCompat.fromHtml / Html.fromHtml、setMessage(resId) 或 android:text 显示带 <b>/<a> 的串，并 setMovementMethod(LinkMovementMethod.getInstance())；写错的样子：鸿蒙端对话框正文写 Text($r('app.string.…')) 或 Text(...) 直接显示，CDATA 文案露出标签原文、链接不可点；或正文链接 Span 只着色不响应点击，另在正文下加一行外链
适用范围：实现阶段渲染安卓带样式字符串（Styled 或 Html 通路）的对话框和页面正文时
做法：
- 用一个公共富文本组件把 b/i/u/small/a/br 和实体解析成 Text 下的 Span，链接 Span 写 .onClick(() => 打开链接)，用 action 'ohos.want.action.viewData' 和链接 uri 的 Want 拉起
- 链接在正文内行内可点，不在正文外另起链接行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare class BaseSpan<T> extends CommonMethod<T>：Span 继承 CommonMethod，可以直接挂 onClick（出处：鸿蒙 SDK 的 ets/component/span.d.ts，BaseSpan）
- 'ohos.want.action.viewData'：查看数据的 Want action；旧模块里的常量 ACTION_VIEW_DATA 已标 @deprecated since 9，直接写字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.ability.wantConstant.d.ts，wantConstant.Action.ACTION_VIEW_DATA）
- 富文本组件分 Styled / Html 两路、链接可点，对话框正文改用它：修好后标签不再露出、正文链接行内可点（出处：卡里修好并验证过）
未核实：卡里环境是 API 24（6.1.1），本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-7456fcf259be55a8834b（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
