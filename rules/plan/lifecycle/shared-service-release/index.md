# 共享服务的停止和最终释放

agent 会看到什么：规格写「页面销毁：取消播放任务并 stop()」、源端清理挂在外层 Composable 的 DisposableEffect 上，切片计划的对接点写「某页面.onDisappear → 共享服务.stop()」

## 规矩

- rule-7936b82568cc｜切片计划不把共享服务的 stop 挂到页面 onDisappear，最终释放写在拥有它的 Ability｜读到：规格写「页面销毁：取消播放任务并 stop()」，源端清理挂在承载多屏的外层 Composable 的 DisposableEffect 上；写错：切片计划的对接点写「某页面.onDisappear → 共享播放服务.stop()」，并把这个回调登记成跨切片编辑或占位
