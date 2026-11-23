# 子页回传结果：来源页用 pushPathByName 的 onPop 接收时，子页成功出栈必须 pop(result)，裸 pop() 不触发 onPop

## 何时使用

跨页回传接线阶段，确定子页成功出栈的调用与来源页读取回传结果的触发点时；规格或基础设施阶段定义回传通道时

## 适用情境

源端用 savedStateHandle 的 addReturn/ConsumeReturn 在子页返回后把结果交给来源页；目标来源页用 NavPathStack.pushPathByName(name, param, onPop) 或共享返回值通道接收，生产页与消费页由不同任务分别实现。

## 例外与边界

- 只给源端会写回传结果的出栈点补 result：源端取消、系统返回等路径不调用 addReturn 时，目标保持不带 result 的出栈，来源页 onPop 不触发正对应源端没有回传；系统返回、侧滑返回本身不带 result，不触发 onPop，需要在取消时也收到通知的，要单独写取消分支，不靠给所有出栈点硬塞 result。

## 原因

onPop 回调只在目标页以 pop(result) 出栈时执行；子页先写共享通道再裸 pop()，消费逻辑放在 onPop 里就永远不运行，新回复、编辑结果与封禁状态都不回显。两端分属不同写者，各自只看到自己那一半；收尾统一回传方式时若只改消费端，也不会暴露。

## 做法

1. 回传通道写清三件事：载荷类型、生产端出栈调用、消费端触发点；走 onPop 时生产端 pop(result)，走共享通道时消费端在 NavDestination.onShown 等回到页面的时机读取。
2. 子页写成功出栈前先查来源页的接收方式（是否带 onPop、判断什么 instanceof 类型），按它要求的实例 pop(result)；同时写共享通道也不省掉 result。
3. 对账时对每个 pushPathByName(..., onPop) 列出目标页全部成功出栈点，确认带 result 且类型与 onPop 判型一致；交接里写“同款”的其他调用点一并检索修改。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、2 步〕pushPathByName、pushDestinationByName 传入的 onPop 回调，仅在 pop、popToName、popToIndex 中设置了 result 参数时触发；不带 result 的 pop() 不触发 onPop
- 〔做法第 2、3 步〕onPop 收到的 PopInfo.result 就是出栈页传入的 result（开发者自定义对象）；PopInfo.info 是触发返回时的页面信息，由系统填入
- 〔原因〕设备上子页以不带 result 的 pop() 出栈时，来源页 pushPathByName 传入的 onPop 回调不执行
- 〔做法第 1 步〕NavDestination.onShown 在该页显示时触发，子页出栈、来源页重新显示时会走到；API 21 起回调带 VisibilityChangeReason
