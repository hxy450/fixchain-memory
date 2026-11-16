# Compose 正文带 LinkAnnotation 链接时，目标用 Span 分段、加链接样式并能点开

审的是：代码
触发（任一种）：
- 读到：源 Compose 正文先转成带 `LinkAnnotation` 的 AnnotatedString（按 URL 链接化的辅助函数）再交给 Text；写错的样子：目标是纯 `Text(<字符串>)`：没有 Span 分段，链接没有颜色和下划线，点了不跳转
适用范围：源端正文里的 URL 被链接化、可点击打开，迁成 ArkUI Text 时
做法：
- 把正文按 URL 切段，写 Text() { ForEach(段, …) { Span(段.text) } }；URL 段加 .fontColor(<源链接色>)、.decoration({ type: TextDecorationType.Underline })，.onClick 里用 UIAbilityContext.openLink(url) 打开
- 对照规格里的链接验收项（URL 可点击跳转），确认已经实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- decoration(value: DecorationStyleInterface): SpanAttribute：Span 的文本装饰线，链接段用 TextDecorationType.Underline（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.decoration）
- Span 的通用事件支持 onClick、onHover：链接段可以直接挂 onClick；Span 没有尺寸信息，ClickEvent.target 无效（出处：ts-basic-components-span.md，事件）
- openLink(link: string, options?: OpenLinkOptions, callback?: AsyncCallback<AbilityResult>): Promise<void>：按链接拉起处理方，返回 Promise（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.openLink）
- URL 按 Span 分段，链接段加颜色和下划线并可 openLink：修复时的做法，复审通过（出处：卡里修好并验证过）
- decoration(value: DecorationStyleInterface): TextAttribute：同族接口：Text 整体的装饰线（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.decoration）
- openLink(link: string, options?: OpenLinkOptions, callback?: AsyncCallback<AbilityResult>): Promise<void>（UIExtensionContext）：同族接口：在 UIExtension 里打开链接（出处：鸿蒙 SDK 的 ets/api/application/UIExtensionContext.d.ts，UIExtensionContext.openLink）
针对本应用要查的：
- 源端链接的颜色和装饰：源工程里生成 AnnotatedString 的那个函数，看 LinkAnnotation 带的 styles 或 SpanStyle；读出颜色（多为 MaterialTheme.colorScheme 的某一项）和是否带下划线，照写到 URL 段的 fontColor、decoration
未核实：卡里的行为出自鸿蒙 SDK API 24，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-5a84af0e2f5c593b9f0c（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 4 ← 诊断
