# 位图按钮不要在同一 Image 上先写图标尺寸再写槽位宽高，槽位放外层 Stack

审的是：代码
触发（任一种）：
- 读到：安卓工具栏按钮是固定宽度承载区里居中显示的 ImageView；写错的样子：同一个 Image 链上先写 .width(…).height(…).objectFit(ImageFit.Contain)，后面又接 .width(…).height(…) 当点击区
适用范围：把工具栏的文字或系统符号按钮换成位图 Image、同时要保留点击热区时
做法：
- 写成 Stack() { Image(<资源>).width(<图标宽>).height(<图标高>).objectFit(ImageFit.Contain) }.width(<槽宽>).height(<槽高>)：点击热区宽高和 onClick 只放在外层 Stack 或 Row 上，Image 只设图标尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 同一组件上后写的 width/height 覆盖先写的值，Image 按整个槽位 Contain 绘制，图标被放大：叠加两组尺寸时只有后一组生效（出处：卡里修好并验证过）
- objectFit(value: ImageFit): ImageAttribute：Image 在自身框内的缩放方式，Contain 按框等比缩放，所以框必须是图标尺寸（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- 改成 Stack 槽位包裹、Image 只设图标尺寸并去掉叠加尺寸后，图标大小恢复正常：按此改后保留（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-b911ada02f4ec55d7d14（刺猬猫阅读）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断；取值 3 ← 诊断
