# 宿主接通弹层内容组件时，逐条执行组件头注写给宿主的义务，如 then 里 requestFocus

审的是：代码
触发（任一种）：
- 读到：弹层内容组件的头注或报告的 Host-side 项写「openCustomDialog().then 里 focusControl.requestFocus(<组件 id>) 兜底」；写错的样子：宿主页 openCustomDialog(...) 之后没有 .then(() => focusControl.requestFocus(...))，弹层打开后输入框没有获焦
适用范围：宿主页接线弹层内容组件时
做法：
- 照头注写 openCustomDialog(content).then(() => { focusControl.requestFocus('<输入框 id>') })；其余写给宿主的义务逐条落实，做不到就上报阻塞
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function requestFocus(value: string): boolean：按 id / key 给指定组件请求焦点（出处：鸿蒙 SDK 的 ets/component/common.d.ts，focusControl.requestFocus）
- 宿主在 openCustomDialog().then 里 requestFocus 后，导入框打开即获焦：修复后的接线（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-1446bd8a3fc8a14b0a94（Sokoban）：做法第 1 步 ← 建议 4、诊断；取值 2 ← 诊断
