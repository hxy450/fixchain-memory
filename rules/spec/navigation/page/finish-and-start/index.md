# 成功后 startActivity 加 finish 的组合跳转

agent 会看到什么：读到源页面对同一次成功既 finish() 又 startActivity(主页) 配 FLAG_ACTIVITY_NEW_TASK（可能分在 EventBus 订阅和 LiveData 回调里）；规格的映射表或验收写成 navPathStack.clear() + pushPathByName、本页 pop 两条独立的导航

## 规矩

- rule-cfde2209573f｜多个安卓导航调用映射到单一 NavPathStack 时，规格写操作前后的栈和兜底，不用 clear() 回主页｜读到：源端成功后 startActivity(主页) 配 FLAG_ACTIVITY_NEW_TASK，同时 finish() 当前页；目标的 Navigation 根内容是启动页；写错：规格的映射表写「NEW_TASK → navPathStack.clear() + pushPathByName(主页)」，没写合并后「操作前栈 → 操作后栈」的净效果，也没写主页不在栈中时怎么办
- rule-600f61df073a｜源页面对同一次成功有多条导航响应时，规格只定义一个导航出口，不拆成独立的出栈和入栈验收｜读到：源 Activity 对同一次成功有两条响应：EventBus 订阅（onEventMainThread）里 finish()，LiveData observe 回调里 startActivity(主页) 配 FLAG_ACTIVITY_NEW_TASK；成功管理器在回调页面前先 post 全局成功事件；写错：规格把两条响应写成两条独立的导航验收：一条要求成功后 navPathStack.clear() + pushPathByName(主页)，另一条要求收到成功事件后本页 pop；两者怎么合并、谁先执行都没定义
