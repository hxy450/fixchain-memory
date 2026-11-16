# 源码迟到结果照常回投时，目标页面结束只记标记，不清空回调和导航栈引用

审的是：代码
触发（任一种）：
- 读到：源码新线程做完后无条件 Handler.post(...) 回 UI，回调里没有 isFinishing() 判断，直接 Toast、startActivity、finish；写错的样子：页面 aboutToDisappear 里调一个 detach 之类的方法，置 destroyed 并清空回调；后台任务完成后 if (destroyed) return，不再提示、不再 pushPathByName
适用范围：后台任务（读卡、网络、文件等）由页面发起、完成时回投 UI，源端不拦截页面结束后的结果
做法：
- aboutToDisappear 只记一个结束标记，保留回调和 NavPathStack 引用；任务完成后照常弹提示、用保留的 NavPathStack 打开下一页，与源端一样
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 页面结束只做标记、保留回调和导航栈引用，迟到结果照常提示并打开下一页：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7d097177e497ea9e202c（MifareClassicTool）：做法第 1 步 ← 诊断；取值 1 ← 诊断
