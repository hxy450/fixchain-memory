# 源端删除并重建整个编辑器再恢复焦点时，目标按数据行整体重建并按序号恢复焦点

审的是：代码
触发（任一种）：
- 读到：源端刷新着色时 removeAllViews() 后重新 init 整个编辑器（按数据行逐个新建 EditText），再按原子项序号 requestFocus()；写错的样子：目标在原地改 fontColor 刷新，ForEach 不按数据行重建，错误的行不随数据消失，也不调 requestFocus 恢复焦点
适用范围：迁移「删除并重建整个编辑器再恢复焦点」的刷新逻辑时（着色更新、保存对话框返回后）
做法：
- 刷新时按当前数据行整体重建编辑器：例如让 ForEach 的 keyGenerator 带上刷新版本号，键一变各行组件重新创建
- 重建后按原来的子项序号恢复焦点：给每行编辑器设 .id(行序号对应的字符串)，再 focusControl.requestFocus(那个 id)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ForEach 的键值变化时，框架基于新键值创建新组件：换键可以触发整体重建（出处：arkts-rendering-control-foreach.md，键值生成规则）
- function requestFocus(value: string): boolean：按组件的 id/key 请求焦点（出处：鸿蒙 SDK 的 ets/component/common.d.ts，focusControl.requestFocus）
- 按数据行整体重建并恢复焦点后，错误的行随数据消失，焦点回到原处：卡里的修法（出处：卡里修好并验证过）
未核实：卡里没记修复用的具体重建和恢复焦点接口；ForEach 换键和 focusControl.requestFocus 是按声明和文档给的写法
来源：1 张卡，1 个应用
- case-4a5592fd88f74b1c16a4（MifareClassicTool）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 3 ← 诊断
