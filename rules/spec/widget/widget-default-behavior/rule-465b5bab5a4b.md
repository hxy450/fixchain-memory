# 源端 setText 预填输入框时，规格写明初始光标在开头、长文本从首行显示

审的是：规格
触发（任一种）：
- 读到：源端 onCreateDialog 或 onCreate 里对 EditText 调 setText(...) 预填；写错的样子：规格的预填只写了填入的值，没写初始光标位置和长文本从哪一行显示
适用范围：规格提取阶段写预填输入框的初始状态时
做法：
- 契约写「光标在开头、长文本从首行显示」，并注明目标 TextInput / TextArea 以 text 预填时光标在末尾、滚到末尾，须显式处理
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- EditText 的默认移动方式是 ArrowKeyMovementMethod，它的 initialize 调 Selection.setSelection(text, 0)：源端 setText 之后光标在开头（出处：android.widget.EditText#getDefaultMovementMethod；android.text.method.ArrowKeyMovementMethod#initialize）
来源：1 张卡，1 个应用
- case-1446bd8a3fc8a14b0a94（Sokoban）：做法第 1 步 ← 建议 2
