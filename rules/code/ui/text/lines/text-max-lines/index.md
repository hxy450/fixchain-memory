# 文字控件的行数限制和省略

agent 会看到什么：源端 TextView 的 android:maxLines / lines / ellipsize、Compose Text 的 maxLines / overflow（或者都没写），对应目标 Text 上的 maxLines、minLines、textOverflow 和测量式截断

## 通用查法

### 文字的行数和截断方式，按控件属性、style 链、默认值查出再写

审的是：代码
触发（任一种）：
- 读到：TextView 或 Compose Text(…) 自身没写 maxLines / lines / ellipsize / overflow；写错的样子：目标 Text 按习惯写 .maxLines(1) 加 TextOverflow.Ellipsis
适用范围：把安卓 TextView 或 Compose Text 迁成 ArkUI Text，定行数和截断方式时
做法：
- 依次查：控件自身的 android:maxLines / lines / singleLine / ellipsize（Compose 是 maxLines、overflow 实参）→ 它引用的 style 及 parent 链、textAppearance 指向的样式 → 都没写取默认（TextView 不限行，Compose Text 不传 overflow 时裁切）
- 按查出的值写：不限行的不写 .maxLines；固定行数写 .minLines(N).maxLines(N)；有上限的写 .maxLines(N)，再按源端截断方式写 .textOverflow({ overflow: 对应的 TextOverflow })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextView 的 mMaximum 初值是 Integer.MAX_VALUE（行数不设上限）：控件、样式都没写 maxLines 时不是 1 行（出处：android.widget.TextView#mMaximum）
- setLines(int lines) 把最少和最多行数都设成 lines：android:lines 是固定行数，不只是上限（出处：android.widget.TextView#setLines）
- TextOverflowOptions.overflow 的 @default 是 TextOverflow.Clip：目标不写截断方式时是裁切，写 Ellipsis 才出省略号（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextOverflowOptions.overflow）
- 默认情况下，文本是自动折行的；指定 maxLines 后最多不超过指定行数：目标不写 maxLines 就和源端一样可折行（出处：ts-basic-components-text.md，maxLines）
针对本应用要查的：
- 源控件实际生效的行数和截断方式：源工程布局 XML 里控件自身的属性；res/values*/styles.xml、themes.xml 里它引用的 style 及其 parent 链、textAppearance 指向的样式；Compose 源码里 Text 调用传的 maxLines、overflow；逐层找到最先给出该属性的那一项；都没写的取平台默认；例：卡里一处 TextView 只引用了 style，顺样式链查出是两行，修成 maxLines(2)
未核实：Compose Text 的 overflow 参数默认是 Clip 出自卡，本机没有 Compose 源码可核；控件自身属性、style、textAppearance 三者谁覆盖谁，族里规矩只按卡里的修法归纳，没有对照 TextView 源码核实
来源：3 张卡，3 个应用
- case-47b9e1107e4e4ecd40bd（AntennaPod）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-5a84af0e2f5c593b9f0c（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-8ec9b17b9de9183f6d89（Privacy Friendly 2048）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4

## 规矩

- rule-423fca9e0bc7｜源 TextView 或 Compose Text 没写行数限制时，目标不加 maxLines(1) 和省略号｜读到：源 TextView 没有 android:maxLines、android:singleLine、android:ellipsize；写错：对应的 Text 加了 .maxLines(1) 和 .textOverflow({ overflow: TextOverflow.Ellipsis })
- rule-904a09286dc6｜控件引用 style 或 Material 控件时，先查样式里的行数、字号字重和 trackColor 再写｜读到：TextView 写 style="@style/…" 或 android:textAppearance，XML 本身没写 maxLines / textSize；写错：目标按「XML 没写即默认」推断成 maxLines(1)，次要文字用一个通用字号键
- rule-96974dce77d9｜android:lines="N" 写成 minLines(N) 加 maxLines(N)，不只写 maxLines｜读到：TextView 写 android:lines="2" 这类固定行数；写错：目标 Text 只写 .maxLines(2)，单行内容时控件变矮
- rule-860fa3006eb7｜Compose Text 有 maxLines 没写 overflow 时，目标用 TextOverflow.Clip｜读到：Compose `Text(…, maxLines = …)` 没有传 overflow 参数；写错：对应的 ArkUI Text 上写了 `.textOverflow({ overflow: TextOverflow.Ellipsis })`，多出省略号
- rule-f63a97164867｜TextView 中间或开头省略时，不退成尾部 Ellipsis，实现测量式中间截断｜读到：TextView 带 android:ellipsize="middle"（或 "start"）且 android:lines="1" / android:maxLines="1"，显示文件名这类尾部有意义的文本，可能还有关键字 Span 高亮；写错：Text 写成 .textOverflow({ overflow: TextOverflow.Ellipsis }) 尾部省略，旁边留 TODO 待确认；或写了不存在的 TextOverflow.MIDDLE
- rule-0214a4ac2f9e｜完整复刻要字符级末行省略时，用 measureTextSize 二分预截「前缀+…」，只换折叠态｜读到：Compose 多行正文 `Text(maxLines = N, overflow = TextOverflow.Ellipsis)`（或 `android:ellipsize`），决策台账要求完整复刻（D0）；写错：目标只写 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })`，折叠态末行按词截断、接「 ...」，和安卓按字符填满接「…」不一致
- rule-9bfe81f8cde2｜didOverflowHeight 决定展开钮时，目标用 measureTextSize 测两次高度比较｜读到：Compose Text 的 onTextLayout { … didOverflowHeight … } 决定是否显示展开/收起按钮，配合 maxLines 切换；写错：目标用字符数阈值判断要不要显示展开钮（如 `.length >` 某个数），没有调用 measureTextSize 之类的实测
- rule-d463d6a349e5｜单行用户内容用 maxLines(1)+Ellipsis 时，补 wordBreak(BREAK_ALL) 按字符省略｜读到：`getSupportActionBar().setTitle(title)` 等工具栏标题，或 android:singleLine / android:ellipsize="end" 的单行文本，内容是用户输入（笔记标题、分类名）；写错：`Text(…).maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })` 没有 .wordBreak(WordBreak.BREAK_ALL)，长英文标题在词边界就省略
- rule-038506293100｜DialogTitle 单行放不下时改中号字两行，目标标题不只写 maxLines(1)｜读到：对话框标题是 com.android.internal.widget.DialogTitle（android:singleLine="true"、ellipsize=end）；写错：目标标题写死 .fontSize(20).maxLines(1)，放不下时只省略，没有改小字号两行的分支
- rule-bcd20efeea05｜源控件是第三方 TextView 子类且无 ellipsize 时，先查库的截断策略，逐行回退省略要自排版｜读到：布局 xmlns 声明了库命名空间，控件是库的 TextView 子类（如 com.neopixl.pixlui.components.textview.TextView），带 android:singleLine 或 android:maxLines，没有 android:ellipsize；写错：目标一律写 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })`，多行正文收起时没有「…」或长标题在词中截断
