# 源端一个 Composable 内多屏共享的清理，拆成多页面后归属外层生命周期，切屏不释放

ID：`lesson-2ed8c21943925bf0ae9a` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时

## 适用情境

源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。

## 例外与边界

- 源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理

## 原因

onDispose 只在所在 Composable 离开组合时触发；外层 Composable 同时承载多屏时，屏间切换只改状态，不触发清理，资源继续存在。把它写成某一页的“页面销毁/退出时 stop()”，就把外层生命周期缩成了单页生命周期，计划与实现照此把释放挂到页面离开回调上。来源中规格、计划、实现依次传递了这一契约；ECAT 静态判定打开子页会打断播放并做了修复，但转录内没有设备复现，该页作为 Navigation 首页内容在推入子页时是否真的触发离开回调未核实。

## 做法

1. 规格提取时，先找清理所在 Composable 承载了哪些屏幕，把清理归属写成承载它们的外层（目标端通常是 Ability 或 Navigation 宿主页），并在跨页对接点写明切到其他屏幕时资源保持。
2. 写“页面销毁/页面退出”类判据前，列出源码里所有会改屏幕状态的入口，确认它们在目标端对应的导航动作不会被写成释放条件。
3. 实现时把共享服务的最终释放放在拥有它的层级（如 EntryAbility.onDestroy），页面离开只解除自身监听；挂到页面回调前先确认页面挂载方式（Navigation 首页内容或 NavPathStack 页面）和推入子页时实际触发的回调。

## 来源（按需复核）

- case-f4de4c0baf567b736a95 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`4a91ed6ed85947112fda96591e5edd557cb0dd09e6db25063b92355193ac95c6`
