# 文本、控件与触摸

读到源端有 TextView、EditText、Slider、WebView 等控件或 Compose Text / TextStyle，onTouch、GestureDetector、SwipeToDismissBox 触摸处理，contentDescription 等无障碍语义，规格里写文本样式、输入约束、控件状态和手势时

## 触发族

- [源码里控件的状态切换和展示加工](widget-state-display/index.md)（4 条）：读到源码里按状态改控件可点、图标、文字色的 setter，点击后成功回调才设选中态，展示文本先经工具函数加工成带链接的文本，标题行名称后带图标和跳转；规格或验收条目只写了文案、数值和颜色
- [Compose Text 和 TextStyle 的文字样式](compose-text-style/index.md)（4 条）：源端 Compose Text(...) 只给 style 不传 color、Typography 的 TextStyle 带 lineHeight 没设 lineHeightStyle，规格里写「默认 onSurface」、排版令牌只列字号行高数值，或把 lineHeight 写成 1:1 直译
- [Compose material3 Slider 的刻度和默认外观](compose-slider/index.md)（3 条）：读到源端 material3 Slider(valueRange = …, steps = …) 或只用 SliderDefaults.colors 传了几种颜色；规格、快照或验收条目里的停靠点数、步长和外观不是按 steps 求值、库默认推出来的
- [安卓触摸监听（onTouch、GestureDetector）的触控契约](touch-listener-contract/index.md)（6 条）：读到源端 onTouch 里 switch (event.getAction()) 分 ACTION_DOWN / MOVE / UP、多个兄弟 View 各自 setOnTouchListener，或 onTouch 只转交 GestureDetector、方向写在 onFling；规格把它逐一对成 TouchType 或只抄阈值，没写附加手指、分指和触发条件
- [WebView 的 WebSettings 配置和导航回调](webview-settings/index.md)（1 条）：读到源端 WebView 用 WebSettings 设 setUseWideViewPort、setLoadWithOverviewMode、cacheMode、mixedContentMode，并有 shouldOverrideUrlLoading；规格映射表里 WebView 只写 loadData 签名和「onLoadIntercept 截获」，标「行为等价」
- [EditText 的 inputType、InputFilter 和分段着色](edittext-input-constraints/index.md)（4 条）：读到布局里 EditText 带 textCapCharacters、numberSigned 等 inputType 标志或 android:digits、maxLength，代码里挂 InputFilter.AllCaps，或以 BufferType.SPANNABLE 放入分段着色的文本；规格写「大写过滤」「无直接等价、放到校验时」「TextArea + Span」这类说法
- [SwipeToDismissBox 的滑删方向](swipe-to-dismiss-direction/index.md)（1 条）：读到源 `SwipeToDismissBox` 写 `enableDismissFromStartToEnd = false`、`SwipeToDismissBoxValue.EndToStart` 才算 dismiss；规格写「EndToStart，即右滑」，或只写枚举名、没写手势方向和 offset 符号
- [多行正文的末行省略（maxLines + Ellipsis）](multiline-ellipsis/index.md)（1 条）：读到源码多行正文写 `maxLines = N, overflow = TextOverflow.Ellipsis` 或 `android:maxLines` 加 `android:ellipsize`；规格转换决策把 `.maxLines(N).textOverflow(...)` 写成「等价」，没写末行截断粒度的差异，也没有 PD 或差异 AC
- [源界面 Text 里的 emoji 字面文本](emoji-in-text/index.md)（1 条）：源端 ListItem 的 leadingContent 等处写 Text("⭐") 这类 emoji 字面文本，上下文另有「图标用 SymbolGlyph」的规则；规格或转换决策表里对 emoji 的处理
- [源组件的无障碍语义（contentDescription、role、合并朗读）](source-a11y-semantics/index.md)（2 条）：读到源端 android:contentDescription 初值取字符串资源、运行时改成拼出的字符串，或 Compose 的 Modifier.clickable(role = Role.Button, enabled = …)、整卡合并的点击区、独立 IconButton、Dialog；规格把喂给 .accessibilityText() 的状态写成 string | Resource，或组件验收条目没写按钮角色、enabled 条件、合并朗读和对话框模态
- [源控件靠框架默认的行为（setError、预填光标、imeOptions）](widget-default-behavior/index.md)（3 条）：读到源控件只写了少数属性、其余靠框架默认：EditText.setError、onCreateDialog / onCreate 里 setText 预填、单行 EditText 不写 imeOptions、WebView 只 loadUrl 不调 getSettings；规格的转换决策只写组件对应，或写成实时校验、行内红字，没写默认行为和目标要显式设的属性
- [源端 onKeyDown 的按键分发和遥控导航](onkeydown-key-dispatch/index.md)（2 条）：读到源端 Activity 或 View 的 onKeyDown 分发音量、相机、媒体键和 SPACE、DPAD、NUMPAD 等键盘键，或用遥控模式标志驱动逐行逐项移动、OK 选择和高亮；规格写「按键交互仅保留屏上控件路径」「DPAD 上下→遥控导航」一句概括，弹层行导航没有验收条目
- [整套迁移的 Markdown 渲染库（Markwon 插件链）](markdown-render-library/index.md)（1 条）：读到源端用 Markwon（以 commonmark 解析为底座）加若干插件渲染 Markdown，Markwon.builder(context).usePlugin(...) 插件链；规格的实现映射写「各插件可观察效果逐一等价」，AC 只覆盖插件和表格、删除线、HTML，没有嵌套列表、惰性续行、松紧列表、引用内块这些 CommonMark 核心语法的契约
