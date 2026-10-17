# ui/state/feedback

操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

[上一级](../index.md)

## 本级经验

- [Toast 时长逐调用点传参，取串后保留加工](lesson-8335bc404934f58c6f31.lesson.md) · 阶段：execute · 信号：Toast.makeText, LENGTH_SHORT, LENGTH_LONG, showToast
- [onErrorReceive 判主框架才切失败态](lesson-051f8984f21058916bd9.lesson.md) · 阶段：execute · 信号：onErrorReceive, isMainFrame(), Web, web.d.ts
- [全局广播浮层按源端队列语义播放不自加去重上限](lesson-2cc8bcca579d597cb6a2.lesson.md) · 阶段：spec/execute/verify · 信号：addAll, remove(0), onAnimationEnd, WindowManager
- [单一 SnackbarHost 用唯一宿主按源排队定时长](lesson-187c725b1bb9d8d1bf4d.lesson.md) · 阶段：execute · 信号：SnackbarHost, Snackbar, actionLabel, SnackbarDuration
- [同一业务链每个入口都调用服务并在终态收口 loading](lesson-a87eaa08f98ea95d04d5.lesson.md) · 阶段：execute · 信号：showLoading, hideLoading, UIContext
- [多来源与次级动作按区块存错误，不整页报错](lesson-a82d821385bf8fb3feb0.lesson.md) · 阶段：execute · 信号：=== null, LiveData, try/catch, Success
- [异步结果回调按成功失败分支列全副作用逐项对齐](lesson-ac7a2e17b8d88c3cee7b.lesson.md) · 阶段：execute/repair · 信号：LiveData, showToast, AlertDialog.Builder, Settings.ACTION_APPLICATION_DETAILS_SETTINGS
- [推迟通知能力时为接口返回数据定义替代去向](lesson-9d54e42c44b0d3e78bb1.lesson.md) · 阶段：spec/plan/execute · 信号：NotificationManager, onData, Toast, showToast
- [校验失败用全局 showToast，页内错误文字放固定行](lesson-f97fc44e58a8d23333f0.lesson.md) · 阶段：execute · 信号：showToast, promptAction, layoutWeight, Toast
- [系统写入降级为保存后成功反馈改为引导手动设置](lesson-e44d598230615f3f3262.lesson.md) · 阶段：execute · 信号：WallpaperManager, RingtoneManager, photoAccessHelper, showToast
