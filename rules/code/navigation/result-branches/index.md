# 异步结果回来后的跳转和提示

agent 会看到什么：读到源 Activity / ViewModel 的成功、失败回调（LiveData observe、Handler.post 回 UI）里的 startActivity、finish、Toast，以及启动 ViewModel 的下一路由决策；产物里替换 FWD-REF 或占位按钮后的结果消费（await、@Monitor）、catch 里的提示、aboutToDisappear 之后的 destroyed 短路、push 到首屏自身

## 规矩

- rule-ba132b153816｜替换 TODO / FWD-REF 占位接线时，按源端回调链落实成功和失败分支的每个动作｜读到：源 Activity 的 initObserve 观察 ViewModel 的完成事件（`LiveData<Boolean>`），成功时写 SharedPreferences 标记、startActivity 跳主页并 finish()，失败时 Toast；目标头注释或 `TODO` 写着「成功后跳 X」；写错：按钮 onClick 只写 this.vm.xxx()，没有 await 结果也没有 @Monitor，成功后不跳转、失败不提示；TODO 被删掉
- rule-e65f2db90774｜源端结果回调的失败分支有 showToast 时，目标失败处同样提示，不只导航或留页｜读到：源 Activity 在 LiveData observe 回调的失败分支里 showToast(R.string.…)，再跳转、finish 或留在当前页（常带一句「失败留在当前页，用户可重试」的注释）；写错：目标的 catch 或失败返回处只有 pushPath / push 跳转，或只有转写过来的留页注释，没有 showToast；ViewModel 的 catch 只 return false，失败被折叠成某个跳转目标
- rule-be6f7feda872｜源码迟到结果照常回投时，目标页面结束只记标记，不清空回调和导航栈引用｜读到：源码新线程做完后无条件 Handler.post(...) 回 UI，回调里没有 isFinishing() 判断，直接 Toast、startActivity、finish；写错：页面 aboutToDisappear 里调一个 detach 之类的方法，置 destroyed 并清空回调；后台任务完成后 if (destroyed) return，不再提示、不再 pushPathByName
- rule-9856e520489b｜启动路由决策仍等于当前首屏时按失败处理，显示可重试的错误，不再 push 自身｜读到：启动 ViewModel 里下一路由的默认值就是首屏自己的路由名；写错：首屏 load().then 后照常 pushPathByName(决策路由)，决策没变时仍是首屏自己，界面停在启动页且没有报错
- rule-6dd4c30963b7｜源端回调把接口返回值交给通知时，页面不能只 await 不接返回值，要回填或提示｜读到：源端接口成功回调把返回数据交给发 Notification 或 Toast 的调用（数据是给用户的验证码，不是可丢弃的发送回执）；写错：页面里 `await` 一个返回 `Promise<string>` 的接口后直接开始倒计时或关弹窗，返回值没赋给任何变量，既没写进 @State 输入框状态，也没有 showToast
- rule-bbcaa0826497｜源端退出分支调 finish() 时，目标在 Toast 结束后 terminateSelf，不写成 pop｜读到：退出分支里 showToast 后调宿主 Activity 的 finish()（外部入口进来时结束页面，而不是回列表）；写错：写成 navPathStack.pop()，注释「无独立任务栈时退化为 pop」
