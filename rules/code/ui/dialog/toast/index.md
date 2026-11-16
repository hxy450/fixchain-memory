# 吐司与提示条

源端有 Toast.makeText、Snackbar / SnackbarHost，目标端有 promptAction.showToast、统一的 ToastService 门面或自绘的提示条时

## 触发族

- [Toast 提示和结果反馈的形式](toast-feedback/index.md)（10 条）：读到源端用 Toast.makeText（LENGTH_SHORT / LONG）、AlertDialog 的去设置引导给校验失败、权限拒绝、写入成功等结果反馈；产物里时长写死、文案少了加工、改成页内错误行或整页错误态、失败一律 showToast，或该弹引导的地方仍弹源端 Toast
- [Compose 的 Snackbar 和 SnackbarHost](compose-snackbar/index.md)（6 条）：读到源端 SnackbarHostState.showSnackbar(message, actionLabel = …) 没写 duration、Scaffold 里只有一个 SnackbarHost，或自定义组件委托 material3 Snackbar；交回的提示条一律 setTimeout 4000、多个底部浮层并存，或几何是凭记忆写死的常量
- [统一吐司门面（ToastService）](toast-facade/index.md)（1 条）：读到计划或审计要求用统一的 ToastService 替换 promptAction.showToast、DialogHelper.showToast 和页面自绘吐司；产物里移动或改写后的页面仍有这些直调，或 @Local 显隐加 Text 覆盖层和 setTimeout 的自绘吐司，公共模块的 Index.ets 没导出门面
- [吐司和 Snackbar 的显示位置](toast-snackbar-position/index.md)（2 条）：读到 Toast.makeText(...).show() 没调 setGravity / setMargin，或 Compose Scaffold 同时带 bottomBar、floatingActionButton 和 SnackbarHost；产物里 showToast 有没有传 bottom、自绘 Snackbar 有没有按底栏和 FAB 留出底部偏移
- [Crouton 提示条的调用和队列](crouton-queue/index.md)（1 条）：读到 Crouton.makeText(activity, message, style, ViewGroup).show()、cancelAllCroutons；产物里页面自持、@Param visible 驱动的单条提示组件，或映射成 promptAction 的 Toast
