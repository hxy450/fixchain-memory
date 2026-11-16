# 公共组件表和 brief 的 PASS

agent 会看到什么：派工给了共享组件表、每行标着安卓 Adapter/item 布局或现有框架组件，brief 写回 final_state: PASS，却没逐个组件指回表里的一行

## 规矩

- rule-80697aa00f48｜brief 写回 PASS 前，每个公共组件都要能指回一条安卓布局或现有框架组件｜读到：派工里给了共享组件表，每行标着安卓 Adapter/item 布局，或标着归属现有框架组件；写错：brief 写回了 `final_state: PASS`，但没有逐个组件写明它对应的安卓布局或现有组件，或者有组件指不回表里任何一行
