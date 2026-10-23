# 源端在相机打开回调里消费一次性拍照请求（快捷方式、桌面卡片）时，目标也在相机就绪回调里消费并沿用延时，不放 aboutToAppear/onPageShow

ID：`lesson-e3bf30ce225c1c8964aa` · 版本：1 · 阶段：spec/execute · 主题：[app/camera/session](index.md)

概要：一次性拍照请求在相机就绪回调消费，不用页面显示

信号：`StateCallback.onOpened`, `onConfigured`, `CameraInput.open`, `aboutToAppear`, `onPageShow`, `onShown`, `onNewWant`

## 何时使用

规格提取与接线阶段，为快捷方式、桌面卡片或外部入口带来的一次性拍照请求确定读取与消费时机时

## 适用情境

源端在相机打开完成（或预览建立）的回调里读取并清除一次性请求标志，再按对焦模式延时触发拍照；目标的相机打开与会话启动在引擎里异步完成，页面生命周期（aboutToAppear、onPageShow/onShown）早于相机就绪；请求标志与引擎回调由不同任务编写。

## 原因

页面显示时相机还没打开，这时消费请求，标志已被清除，拍照又因相机未就绪被拒绝，请求就此丢失，冷启动和从后台返回都不出照片。引擎回调里把源端读取写成常量后，按对焦模式延时拍照的分支也永远不会执行。

## 做法

1. 规格的目标锚点与对接点落在目标的相机打开/预览启动完成回调，与源端回调对应；写完核对验收项正文的时序（如“相机打开后”）与锚点一致。
2. 消费放进该回调：读后即清，沿用源端按对焦模式的延时后，走源端同一拍照入口；不改走受定时、重复拍照偏好影响的快门按钮入口。
3. 请求标志归其他任务时，引擎回调里留读取/消费的注入点并登记，不写常量 false；页面隐藏或销毁时作废未消费的请求。

## 可选检查

- 在设备上分别冷启动和从后台返回后触发入口，各应新增一张照片；页面显示后立即拍照被拒绝，说明消费点早于相机就绪。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [卡片字号图标按源 sp/dp 等值，不放大](../../../ui/text/typography/lesson-4c8d66cb58e835e61c3e.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-9720ed67e580c21dbd65](../../../../../store/cases/case-9720ed67e580c21dbd65/e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602.json) · 结论：diagnosis, rec-d493e8937b, rec-db6378998d, rec-be8e730b62, rec-b21e154125
  卡片版本：`e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602`
