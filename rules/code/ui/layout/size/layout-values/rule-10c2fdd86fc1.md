# 根布局高度是固定 dimen 时用 height()，不写成 constraintSize minHeight

审的是：代码
触发（任一种）：
- 读到：源布局根节点 `android:layout_height="@dimen/…"`（具体尺寸，不是 `wrap_content`）；写错的样子：目标根节点写 `.constraintSize({ minHeight: ... })`，内容多时会被撑高
适用范围：源布局的根或列表项根节点高度是固定 dimen 时
做法：
- 写 .height(<该 dimen 的 vp 值>)；只有源端是 android:minHeight 时才用 constraintSize({ minHeight })，两者分开核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- height(value: Length): T：固定组件高度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.height）
- constraintSize(value: ConstraintSizeOptions): T，默认 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}：只限定尺寸范围，minHeight 不固定高度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.constraintSize）
- 根高从 constraintSize({ minHeight }) 改回固定 height 后与源端一致：验证过的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 这个 dimen 的值：源工程 res/values*/dimens.xml 里按 dimen 名找，留意 values-sw*、values-land 等限定目录的覆盖；dp 值直接作为 vp；有多个限定目录的分别写成目标端对应的资源
来源：1 张卡，1 个应用
- case-9cfde635e67a08373fe6（omni-notes-hmos）：做法第 1 步 ← 建议 5；取值 3 ← 诊断
