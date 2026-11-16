# 源端条目带 CheckBox 切换完成状态时，目标写 Checkbox.select 加 onChange

审的是：代码
触发（任一种）：
- 读到：源端列表条目里 `CheckBox` 的 `isChecked = item.isCompleted`，点击回调调用 ViewModel 的切换方法，再由它调仓库层写入完成状态；写错的样子：目标条目的 `@Builder` 里没有 `Checkbox`，或有 `Checkbox` 没有 `.onChange(...)`；对应 ViewModel 只有 `loadData`/`refresh`，缺切换完成状态的方法
适用范围：把带完成勾选框的安卓列表条目迁成 ArkUI 列表项及其 ViewModel 时
做法：
- 条目里写 `Checkbox().select(item.isCompleted).onChange((value: boolean) => { this.vm.切换方法(item.id, value) })`
- 同一轮给 ViewModel 补上切换方法：调仓库层写入完成状态后重载数据
- 写条目和 ViewModel 前，按切片计划的 spec_ref 和 page spec 路径重读原文（上下文压缩后续跑时必须重读），把条目的每个控件和交互列成清单再写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- select(value: boolean): CheckboxAttribute：设置勾选框是否选中（出处：鸿蒙 SDK 的 ets/component/checkbox.d.ts，CheckboxAttribute.select）
- onChange(callback: OnCheckboxChangeCallback): CheckboxAttribute；type OnCheckboxChangeCallback = (value: boolean) => void：选中状态变化回调，参数是新的选中值（出处：鸿蒙 SDK 的 ets/component/checkbox.d.ts，CheckboxAttribute.onChange）
- 条目前置 Checkbox().onChange → ViewModel 切换方法 → 仓库层写入并重载，编译通过、功能恢复：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-48d580c7ac15b8131c0f（星途清单）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 1；取值 3 ← 诊断
