# 源 RecyclerView 无背景叠在头图上时，目标滚动内容层保持透明，只给卡片设背景

审的是：代码
触发（任一种）：
- 读到：布局里头图 ImageView 在下层，SwipeRefreshLayout / RecyclerView 和根容器都没有 android:background，叠在头图之上；写错的样子：Stack 里位于头图 Image 之上的全高 List（height('100%')）设了不透明 .backgroundColor(...)，头图被完全遮住
适用范围：源端内容列表透明叠在头图上、目标用 Stack 叠放头图和滚动内容时
做法：
- 滚动内容层（List、Scroll）不设背景或设 .backgroundColor(Color.Transparent)，背景只设在各卡片自身的节点上
- 写完逐层核对：Stack 里位于头图之上的全高容器有没有不透明 backgroundColor
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Stack 的子组件按顺序依次入栈，后一个子组件覆盖前一个子组件：写在头图之后的内容层盖在头图上（出处：ts-container-stack.md，页首说明）
- backgroundColor(value: ResourceColor): T：背景色属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundColor）
- Color.Transparent：透明色枚举值（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Color.Transparent）
- 内容 List 背景改为 Transparent 后头图露出：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-5d12548f9d559985c27d（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
