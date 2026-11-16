# 统一吐司门面（ToastService）

agent 会看到什么：读到计划或审计要求用统一的 ToastService 替换 promptAction.showToast、DialogHelper.showToast 和页面自绘吐司；产物里移动或改写后的页面仍有这些直调，或 @Local 显隐加 Text 覆盖层和 setTimeout 的自绘吐司，公共模块的 Index.ets 没导出门面

## 规矩

- rule-30b47091f83a｜计划要求统一吐司门面时，移动或下沉页面前先建门面并把页面里的直调改成调门面｜读到：计划或审计要求用统一 `ToastService`（全局吐司管理）替换 `promptAction.showToast`、`DialogHelper.showToast` 和页面自绘吐司，业务侧直调归零；写错：移动或改写后的页面里仍有 `promptAction.showToast(`、`DialogHelper.showToast(`，或页面私有 `@Local` 显隐状态加 `Text` 覆盖层和 `setTimeout` 的自绘吐司；公共模块的 `Index.ets` 导出了别的工具，却没有吐司门面
