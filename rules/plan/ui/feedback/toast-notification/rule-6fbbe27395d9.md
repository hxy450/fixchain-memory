# 计划替换清单里有吐司统一和直调归零时，收口前逐行转成本批检查项并计数

审的是：计划与派工
触发（任一种）：
- 读到：已批准的计划或审计的替换清单里有「直接 Toast → 统一 ToastService → 对应业务完成时调用数归零」这类横切行；写错的样子：批次的检查项或收口报告只列了同批的静态项（如 LazyForEach→Repeat）通过，没有吐司直调的计数，也没有逐项豁免登记
适用范围：执行业务批次或全量收口、计划里带横切替换清单时，本批检查项和收口报告
做法：
- 开工前把计划替换清单逐行转成本批检查项，横切行与 LazyForEach→Repeat 这类静态项同等对待
- 收尾时用 rg 统计 `promptAction.showToast`、`getPromptAction().showToast`、`DialogHelper.showToast` 以及页面私有的吐司显隐状态加 Text 覆盖层，结果为 0 或逐项登记豁免后才写收口通过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function showToast(options: ShowToastOptions): void（@deprecated since 18，@useinstead ohos.arkui.UIContext.PromptAction#showToast）：模块级的吐司直调；它和 UIContext 上的 getPromptAction().showToast 都要计入直调（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，promptAction.showToast）
- showToast(options: promptAction.ShowToastOptions): void：UIContext 取得的 PromptAction 上的吐司直调（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.showToast）
来源：1 张卡，1 个应用
- case-60960b31a847ea9bb8c7（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
