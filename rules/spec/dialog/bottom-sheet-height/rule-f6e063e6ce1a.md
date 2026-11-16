# BottomSheetDialogFragment 的弹层高度看方法体判定，没改高度的写 FIT_CONTENT

审的是：规格
触发（任一种）：
- 读到：BottomSheetDialogFragment 的 onShow 里调了名为 setupFullHeight 之类的方法，方法体只把 getLayoutParams() 原样 setLayoutParams 回去，再 setState(STATE_EXPANDED)；写错的样子：规格按方法名写“全高展开”，转换决策给 detents:[SheetSize.LARGE] 或“detents 全高”
- 读到：BottomSheetDialogFragment 没有改 peekHeight、state 和高度；写错的样子：规格或头注释写“默认半开/全开”，给 detents:[SheetSize.MEDIUM, SheetSize.LARGE]
适用范围：规格提取阶段把 Material BottomSheetDialogFragment 映射为 ArkUI bindSheet、确定弹层高度时
做法：
- 看方法体，不看方法名：只 setState(STATE_EXPANDED)、LayoutParams 原样回填，或根本没改 peek/state 的，规格写“按内容高度完整展开”，映射为 height: SheetSize.FIT_CONTENT
- 只有看到 setLayoutParams 改成 MATCH_PARENT、setPeekHeight、skipCollapsed 等实际改高度的代码，才写全高或多档 detents；拿不准时把源根布局的高度写进待核对登记
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SheetSize.FIT_CONTENT = 2：弹层高度自适应内容：源端按内容高度展开的弹层对应这一档（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetSize.FIT_CONTENT）
- SheetOptions.height 默认 SheetSize.LARGE：规格不写高度时宿主不写 height 就是大档，所以要明确写 FIT_CONTENT（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.height）
- 改成 height: SheetSize.FIT_CONTENT 后，原来悬在中部或撑到全高的弹层按内容高度显示，与源端一致：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源弹层是否真的改了高度：源工程里这个 BottomSheetDialogFragment 子类的 onCreateDialog / onShow 监听，以及它调用的辅助方法的方法体；找 setLayoutParams 的参数是否改成 MATCH_PARENT、有没有 setPeekHeight、setSkipCollapsed；都没有就按内容高度
未核实：卡里的实测分别出自 HarmonyOS 6.1.0（API 23）和 6.0.2（API 22）两个环境
来源：1 张卡，1 个应用
- case-1ff61bb8eea97c7cac7f（AntennaPod）：做法第 1 步 ← 建议 1、建议 5；做法第 2 步 ← 建议 1、建议 5；取值 3 ← 诊断
