# removeAllViews 后逐项 addView 重建的行

agent 会看到什么：读过的源码里每次计算或刷新先 removeAllViews()，再循环 inflate / addView 重建结果行或整个编辑器、按序号 requestFocus；交回的 ForEach 键只用显示内容拼、不含序号或代次，或原地改属性不重建、不恢复焦点

## 规矩

- rule-de9ace3efccd｜结果每次整体重建、条目是普通 class 时，ForEach 键加每次计算的代次前缀｜读到：源端每次计算先 removeAllViews() 再整体重建结果区；写错：渲染模型是普通 class（没有 @ObservedV2 / @Trace），ForEach 的键不含代次，两次计算的条目键相同时复用旧行、显示旧数据
- rule-8a7ebcc3e350｜removeAllViews 后逐项 addView 的行内容可能重复时，ForEach 键带位置标识｜读到：源端一次计算里 removeAllViews() 后循环 inflate / addView 结果行，行内容可能完全相同（如多个相同的数据块）；写错：ForEach 的 keyGenerator 只用显示内容拼键（如 `${a}_${b}_${c}`），不含条目序号；渲染模型 class 没有唯一标识字段
- rule-3177f7aef5df｜源端删除并重建整个编辑器再恢复焦点时，目标按数据行整体重建并按序号恢复焦点｜读到：源端刷新着色时 removeAllViews() 后重新 init 整个编辑器（按数据行逐个新建 EditText），再按原子项序号 requestFocus()；写错：目标在原地改 fontColor 刷新，ForEach 不按数据行重建，错误的行不随数据消失，也不调 requestFocus 恢复焦点
