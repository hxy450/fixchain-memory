# 同一视图要圆角加描边时，圆角写进 border 的 radius，不在前面单写 borderRadius

审的是：代码
触发（任一种）：
- 读到：同一视图同时有圆角和描边：MaterialButton 的 app:cornerRadius + app:strokeColor / app:strokeWidth、CardView 的 app:cardCornerRadius 加描边、TextInputLayout 的 OutlinedBox 样式；写错的样子：.borderRadius(X) 之后紧跟不带 radius 的 .border({ width, color })
适用范围：目标组件同时需要圆角和边框时的修饰链
做法：
- 写成 .border({ width, color, radius: X })，或保证 .borderRadius(X) 在 .border() 之后
- 写完 grep「.borderRadius( 之后紧跟不含 radius 的 .border({」这一组合，逐处改掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- color、radius 缺省时，要保证 borderColor、borderRadius 生效，需把它们设在 border 之后：border 不带 radius 会把前面的 borderRadius 盖掉（出处：ts-universal-attributes-border.md，border）
- border(value: BorderOptions): T；BorderOptions.radius?: BorderRadiuses | Length | LocalizedBorderRadiuses：圆角可以直接写在 border 里（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.border；ets/component/units.d.ts，BorderOptions.radius）
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T：单独设圆角（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- 把 borderRadius 的值写进 border 的 radius：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 4 ← 诊断
