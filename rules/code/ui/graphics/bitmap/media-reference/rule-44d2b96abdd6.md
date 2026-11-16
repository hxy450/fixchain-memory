# 目标位图颜色与源端不一致时，先查是不是用错了资源，不用 fillColor 给替代图着色

审的是：代码
触发（任一种）：
- 读到：源端 ImageView 的 android:src 或背景用的位图本身带颜色；写错的样子：目标的 Image($r('app.media.…')) 逐个加了 .fillColor('#…') 去模仿原图颜色
适用范围：迁移位图图标、目标显示颜色与 Android 不一致时
做法：
- 先核对引用的是不是原图（按原名、文件大小或哈希），换回原图并去掉 .fillColor；原图本身带颜色时不再二次着色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute：声明写明这个属性只对 SVG 图生效，位图上不起作用（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 换回原名位图并去掉全部 fillColor 后颜色与源一致：修好的结果（出处：卡里修好并验证过）
未核实：卡里被着色的替代图是位图还是 SVG 没写明
来源：1 张卡，1 个应用
- case-9394dee6fa8ae478e54c（刺猬猫阅读）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
