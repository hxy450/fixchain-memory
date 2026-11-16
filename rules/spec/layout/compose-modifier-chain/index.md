# Compose 修饰符链里的内距、背景和尺寸

agent 会看到什么：读过的 Compose 源码里 Modifier 链上 padding / statusBarsPadding / navigationBarsPadding 与 background、heightIn、size 有先后，或 LazyRow 的 contentPadding、M3 IconButton 外层 .size(x)；交回的规格把这些平列，或把修饰符字面当实绘尺寸

## 规矩

- rule-f27c633ae749｜规格描述带背景的组件时，按修饰符顺序写明内距或 inset 在背景之内还是之外｜读到：Compose 源码里 Modifier 链的 padding、statusBarsPadding 与 background、shape（或 Surface 包装）有先后顺序；写错：规格把 padding、底色、圆角写成并列属性（「高 …dp，…padding：Surface 容器（…底色，…圆角）」「minHeight …、statusBarsPadding、…底」），没写内距在背景之内还是之外
- rule-6fd12e8cbe9e｜规格写 Compose 修饰符链时写明内距和最小高度的先后，不只平列各项｜读到：源码 Modifier.navigationBarsPadding().then(…).heightIn(min = N.dp) 这类内距与 heightIn 串在一条链上；写错：规格只平列「navigationBarsPadding、水平 24dp、minHeight 56dp」，没写先后，看不出最小高度在内距之内还是之外
- rule-56f87b2775c8｜规格描述 LazyRow/LazyColumn 时，把 contentPadding 写成「内容内距（滚动时不裁切）」｜读到：Compose 的 LazyRow / LazyColumn 写了 contentPadding = PaddingValues(start = …, end = …)；写错：规格只写「左右 padding」，没区分列表的内容内距和普通外框 padding
- rule-d524b225a70a｜M3 IconButton 外层写 .size(x) 且 x<48 时，规格按实绘 48 记并以圆心描述位置｜读到：Compose 源码 IconButton(onClick = …, modifier = Modifier….size(x.dp)….background(…, CircleShape))，x < 48（如 36.dp）；写错：转换决策表把修饰符字面当实绘尺寸，写成 .width(36).height(36) 或「size 36 圆底按钮」，位置按左上角（距左 16、距状态栏 10）描述，没标低置信
- rule-f6018af5ba1f｜Compose Row 里不带 weight 的 fillMaxWidth 子项后还有兄弟时，规格标「源码有、实绘无」｜读到：Compose Row { …; Text(modifier = Modifier.fillMaxWidth()…); IconButton { … } }：不带 weight 的 fillMaxWidth() 子项后面还跟着兄弟组件；Column 里不带 weight 的 fillMaxHeight() 子项同理；写错：规格的页面结构、clickable_elements 或合成的 view.xml 把这个兄弟列为可见、可点的元素，转换决策还给它写了映射（.enabled / .opacity / .fontWeight）
