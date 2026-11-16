# 源 TextView 或 Compose Text 没写行数限制时，目标不加 maxLines(1) 和省略号

审的是：代码
触发（任一种）：
- 读到：源 TextView 没有 android:maxLines、android:singleLine、android:ellipsize；写错的样子：对应的 Text 加了 .maxLines(1) 和 .textOverflow({ overflow: TextOverflow.Ellipsis })
- 读到：Compose 源里 Text 只有 Modifier.weight(1f)，没有 maxLines / overflow；写错的样子：目标 Text 加了 .maxLines(1) 和 .textOverflow({ overflow: TextOverflow.Ellipsis })
适用范围：把安卓 TextView（含列表行、组头里的）或 Compose 列表行里的 Text 迁成 ArkUI Text 时
做法：
- 不写 maxLines 和 textOverflow，让 Text 保持默认的自动折行，按内容换行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 默认情况下，文本是自动折行的；指定 maxLines 后最多不超过指定行数：不写 maxLines 就和源端一样可折行（出处：ts-basic-components-text.md，maxLines）
- maxLines(value: number): TextAttribute：只有源端写了行数限制时才用（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.maxLines）
- 名称不限行：修好后长名称换行显示，与源一致（出处：卡里修好并验证过）
来源：2 张卡，2 个应用
- case-036361d8949e7daf5247（Cofi）：做法第 1 步 ← 诊断；取值 3 ← 诊断
- case-8ec9b17b9de9183f6d89（Privacy Friendly 2048）：做法第 1 步 ← 建议 4、诊断
