# 弹窗内容面板包着可点子控件时不用 HitTestMode.Block，防穿透只放在无子控件的遮罩上

审的是：代码
触发（任一种）：
- 写错的样子：弹窗或底部面板的内容 Column、根 Stack 上写 .hitTestBehavior(HitTestMode.Block)，里面有 Button、Checkbox、列表项等要点击的子控件
适用范围：ArkUI 弹窗或浮层采用「根 Stack + 遮罩 + 内容面板」结构、用 hitTestBehavior 防点击穿透时
做法：
- 防穿透只写在没有子控件的遮罩层上（.hitTestBehavior(HitTestMode.Block)，或 Default 加 onClick）；承载按钮、Checkbox、列表的内容面板和根容器保持 HitTestMode.Default；要把事件让给下层时用 Transparent 或 None
- 在一处发现 Block 吞掉子项点击后，搜 HitTestMode.Block 扫一遍同类弹窗和浮层，逐个确认它有没有包住可点击的子控件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HitTestMode.Block：自己响应，但阻断子节点和被它盖住的其他节点的命中测试；包住按钮时按钮点不到（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Block）
- HitTestMode.Default：自己和子节点都响应，阻断被它盖住的其他节点；hitTestBehavior 不写时就是它（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Default）
- hitTestBehavior(value: HitTestMode): T：组件的命中测试方式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- 删去包住按钮的内容 Column 上的 Block 后按钮命中；Sheet 内容去掉 Block、根改 Default 后 Checkbox 和整行点击通过：卡里的修法，真机复测通过（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8c39ab17c6d5d6951b85（记得日历）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 4；取值 4 ← 诊断
