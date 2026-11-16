# 翻译服务未落地时保留 FWD-REF 并写明原因，目标实现写进页面才列 resolved

审的是：计划与派工
触发（任一种）：
- 读到：marker 注释或页面规格写明了目标实现（运行期翻译服务的 t()），执行规范要求 forward-ref「marker 消失 + 真实实现存在」；写错的样子：回执把该 P-ID 列进 `resolved_fwd_refs`、称「marker 全部消失 + 真实实现落地」，而页面里没有调用目标实现；或者服务还没落地就删了 marker，`uncertain_regions_retained` 里没写
适用范围：切片 worker 的回执里 forward-ref 的解除和保留
做法：
- 服务确实没落地时保留 FWD-REF marker（或改指向服务所属切片、closer），在回执 `uncertain_regions_retained` 写明原因
- 只有 marker 或页面规格写明的目标实现真正写进页面，才把该 P-ID 列入 `resolved_fwd_refs`
来源：1 张卡，1 个应用
- case-94947376da10a8057b81（Countdate）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
