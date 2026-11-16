# Crouton 提示条的调用和队列

agent 会看到什么：读到 Crouton.makeText(activity, message, style, ViewGroup).show()、cancelAllCroutons；产物里页面自持、@Param visible 驱动的单条提示组件，或映射成 promptAction 的 Toast

## 规矩

- rule-00ea6fe614a8｜源端 Crouton.makeText(…).show() 迁成全局单例队列加宿主组件，并提供 cancelAll｜读到：源端调用 Crouton.makeText(activity, message, style, 容器 ViewGroup).show()，带容器句柄；写错：目标端是页面自持、@Param visible 驱动的单条提示组件，没有队列和 cancelAll，隐藏延迟只用 duration；或映射成 promptAction 的 Toast
