# 规格把 AlertDialog（含列表选择）映射为居中模态对话框，不写 bindSheet

审的是：规格
触发（任一种）：
- 读到：源码 new AlertDialog.Builder…setTitle(...).setView(ListView).create() 的列表选择对话框；写错的样子：规格的组件映射写“bindSheet 半模态 + List（或 Menu）”，理由写“选择类交互更贴近”
适用范围：规格提取阶段给 AlertDialog 选目标承载形态时
做法：
- 规格里写：AlertDialog（含 setView(ListView) 列表选择）→ 居中模态对话框，列表在对话框内容里，标题保留；不写 bindSheet 半模态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindSheet 绑定的是半模态页面：和居中对话框是两种形态（出处：ts-universal-attributes-sheet-transition.md，半模态转场）
来源：1 张卡，1 个应用
- case-48eaca54675fe3fdc6e9（MifareClassicTool）：做法第 1 步 ← 建议 4
