# 跳转前后的附带动作

agent 会看到什么：读到源端 startActivity 之前写共享状态（播放队列、Store）、点击浮层只跳转不动队列、激励广告回调之后才导航；产物里 push 前后少了或多了动作：没写队列、清空了队列、只写 Store 不 push、能力不可用时直接 return

## 规矩

- rule-f349670f9b0d｜源端 startActivity 前先写播放队列等共享状态时，目标在 push 前按同序写入｜读到：源端列表项点击处理在 startActivity(Intent) 之前，先把当前列表（过滤掉广告等项）和新位置交给共享播放器 / ViewModel 的队列写入方法，再带 id 类参数启动播放页；写错：目标只构造页面参数（id、type）后 pushPathByName(...) 或 router.pushUrl(...)，跳转前没有调用工程已有全局引擎的队列写入方法
- rule-c3468d2a7030｜功能规格写结果交给 Store、页面 spec 写成功后进结果页时，写完 Store 再 push 结果页｜读到：源端保存成功后 startActivity 启动结果页并带来源类型；页面 spec 写「成功后进入结果页」，功能规格只写「结果交给 Store」「不新建重复路由栈」；写错：导出成功回调里只把结果写进共享 Store，没有 HMRouterMgr.push 到已注册的结果页
- rule-9a43245e624e｜源端点击浮层只跳转、不动队列时，目标点击回调里不清空剩余队列｜读到：源端浮层根布局的 setOnClickListener 里只埋点并 startActivity(intent) 跳详情，不改队列 List；写错：目标的 onClick 回调里先清掉当前项和剩余队列，再跳转
- rule-18df4e831994｜奖励门的能力不可用分支显式提示后继续导航，不伪造 REWARDED，也不和关闭、失败一起 return｜读到：源端入口先调激励广告、只在 onReward 回调后导航；修复单要求能力不可用时阻断，而通用条款写「显式失败/禁止伪成功只约束失败路径语义，禁止把未配置实现成功能整片不可用」；写错：入口 handler 里 UNAVAILABLE 和 DISMISSED、FAILED 一起进 if (!canContinue) { 提示; return }，广告 provider 未装配时入口点了只出提示、停在原页
