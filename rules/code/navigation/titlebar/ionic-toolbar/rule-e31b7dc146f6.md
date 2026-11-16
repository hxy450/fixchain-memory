# 复用已有头部写法前核对源端标题对齐，Ionic iOS 的 IonTitle 全宽居中

审的是：代码
触发（任一种）：
- 读到：源 IonToolbar 里 IonTitle 加 slot="end" 的按钮（Ionic iOS 模式）；写错的样子：目标头部 Row 里标题只有 .layoutWeight(1)，没有居中，end 按钮挤占了居中空间
适用范围：Ionic iOS 模式的工具栏迁成 ArkUI 头部、又想沿用工程里已有的头部写法时
做法：
- 头部写成 Stack：标题 .width('100%').textAlign(TextAlign.Center) 全宽居中，slot=end 的按钮叠在右侧，不占居中空间
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 头部改成 Stack 全宽居中，标题加 textAlign Center：修复后标题与源端一样居中（出处：卡里修好并验证过）
针对本应用要查的：
- 工具栏、标题的默认度量（padding、字号）：源工程 node_modules 里 @ionic/core 的 css，按 ion-toolbar、ion-title 的 ios 模式选择器找；读出 padding、font-size、min-height 换成 vp / fp 写进头部
来源：1 张卡，1 个应用
- case-acd91ce1ab3d2798a4fa（Countdate）：做法第 1 步 ← 建议 4、诊断；取值 1 ← 诊断
