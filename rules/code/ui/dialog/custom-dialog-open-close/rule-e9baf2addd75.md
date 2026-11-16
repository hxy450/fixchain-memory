# 页内浮层改成 DialogHelper 真弹窗后，删掉全部自绘遮罩和 Block 防穿透写法

审的是：代码
触发（任一种）：
- 写错的样子：改成 DialogHelper.showCustomDialog / showBindSheet 后，弹窗内容根仍有 .hitTestBehavior(HitTestMode.Block)，或根 Stack 还留着 visible ? HitTestMode.Block : HitTestMode.None
适用范围：把页内自绘的弹窗、底部面板迁到 harmony-dialog（DialogHelper.showCustomDialog / showBindSheet），由框架提供模态遮罩时
做法：
- 迁移后删掉全部自绘遮罩，以及内容根和根容器上的 Block、visible ? Block : None 防穿透写法；模态遮罩和外部点击交给弹窗选项（如 isModal、maskColor）
- 对照同仓已有的 customDialog / bindSheet 内容，检查目标控件的整条祖先链上都没有 Block
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 同仓已用 showBindSheet 的弹窗内容 Column 与按钮行都不写 Block；删掉保留的 Block 后子控件点击恢复：卡里的参照和修法（出处：卡里修好并验证过）
针对本应用要查的：
- 弹窗库里控制模态遮罩的选项：目标工程依赖的 harmony-dialog 包里弹窗选项的定义（BaseDialogOptions 一类），或同仓已有弹窗的选项写法；找到模态和遮罩颜色的选项名，按同仓已有写法设置
未核实：harmony-dialog 的 isModal、maskColor 等选项出自卡里读到的同仓代码，本机没有核对该库的声明
来源：1 张卡，1 个应用
- case-8c39ab17c6d5d6951b85（记得日历）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
