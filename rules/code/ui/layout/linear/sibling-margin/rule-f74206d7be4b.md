# 等权重兄弟带 marginStart 作间距时，间距移到 Row 的 space，不写在 layoutWeight 项上

审的是：代码
触发（任一种）：
- 读到：水平 LinearLayout 里同级子项都是 android:layout_width="0dp" + android:layout_weight="1"，其中一项用 android:layout_marginStart / layout_marginEnd 承担卡间距；写错的样子：等权重兄弟写成 .layoutWeight(1)，其中一项另带 .margin({ left: <间距> })（或 start / right），各卡宽度不相等
适用范围：源端等权重的 LinearLayout 子项靠某一项的 margin 留间距，迁成 ArkUI Row / Column 加 layoutWeight 时
做法：
- 去掉权重项上的 margin，间距写到父容器：Row({ space: <源端间距 dp 值> })（纵向用 Column({ space: ... })），或在两项之间放固定宽的 Blank；layoutWeight 只分配扣除间距后的宽度
- 写完按 (容器宽 − 间距) / 权重和 算一遍，各项宽度应相等
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ArkUI 的 layoutWeight 份额包含子项自身的 margin：带 margin 的那项内容宽少一个间距；改成 Row({ space }) 后两卡等宽：两平台权重分配的差别（出处：卡里修好并验证过）
- LinearLayout 先把各子项的 leftMargin + rightMargin 计入总长，再把剩余空间按权重分给 0dp 子项：源端的权重份额不含 margin（出处：android.widget.LinearLayout#measureHorizontal）
- space?: string | number，单位 vp，默认 0：Row 的子项间距（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowOptions.space；ts-container-row.md，RowOptions）
- space?: string | number：同族接口：Column 的子项间距（出处：鸿蒙 SDK 的 ets/component/column.d.ts，ColumnOptions.space）
- layoutWeight(value: number | string): T，从主轴剩余空间按权重分配尺寸，分配时忽略元素本身的尺寸设置：目标端的权重分配（出处：ts-universal-attributes-size.md，layoutWeight）
未核实：卡里的观察出自 HarmonyOS 6.1.1(24)，本机核对声明用的是 API 23
来源：1 张卡，1 个应用
- case-eac486f2e51124dda2cb（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断、建议 2
