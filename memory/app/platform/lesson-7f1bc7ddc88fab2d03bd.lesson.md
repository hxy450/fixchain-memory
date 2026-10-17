# 源端定时提醒迁 reminderAgentManager 时按其自身 d.ts 映射按钮与贪睡，并写出发布失败、条数上限与到点无回调的回退

ID：`lesson-7f1bc7ddc88fab2d03bd` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与决策阶段，为源端 AlarmManager 定时提醒（带贪睡、延后、打开条目按钮的通知）选定代理提醒等替代路径时；实现阶段按规格写提醒调度与按钮处理时

## 适用情境

源端到点由 AlarmManager/广播触发，应用自己构建带按钮的通知，按钮经 PendingIntent 拉起透明跳板 Activity 做贪睡、延后或打开条目，提醒数不设上限、可链式重挂。目标规格准备以“系统托管”整体替代，把 notificationManager 的 NotificationActionButton.wantAgent 写进 reminderAgentManager 的 ActionButton；或实现者发现规格与 d.ts 冲突后改用系统 CLOSE/SNOOZE 按钮作“最大近似”。

## 例外与边界

- 源端只需系统模板提醒：没有路由到应用的按钮、没有自定义贪睡间隔，发布失败时源端也不补偿

## 原因

代理提醒由系统渲染与触发：到点不回调应用，三方可用的按钮只有系统类型，贪睡间隔、条数配额与发布权限都受平台约束。把另一模块的按钮字段嫁接过来，规格写出不可达的按钮路由；实现者再用系统按钮收口，贪睡、延后、打开条目只剩通知体一条入口，发布失败或超限时提醒静默丢失。

## 做法

1. 写替代路径前逐字段对照目标模块自己的 d.ts：reminderAgentManager.ActionButton 在项目 SDK 中三方可用的字段与 ActionButtonType 枚举（带 @systemapi 的成员不算可用）；按钮跳转所需的 wantAgent 在 notificationManager 的 NotificationActionButton 上，不跨模块嫁接字段。
2. 在同一映射行写出平台事实，再决定是否需要应用侧回退：贪睡用 ReminderRequest 的 timeInterval（单位秒，源端分钟偏好×60）与 snoozeTimes；三方应用有效提醒上限 30 条（华为开发者文档「代理提醒」约束说明，以所用 API 版本为准）；publishReminder 的失败错误码（见 d.ts 与错误码文档）及 ohos.permission.PUBLISH_AGENT_REMINDER 权限，未开通代理提醒能力的设备上发布可能恒失败；到点不回调应用；按钮状态回调接口以项目 d.ts 为准。
3. 源端按钮要路由到应用（打开条目、延后选时间）时，走 notificationManager 本地通知的 NotificationActionButton.wantAgent，或项目 d.ts 提供的提醒按钮状态订阅；不以系统 SNOOZE/CLOSE 按钮代替应用侧动作。
4. publishReminder 失败或超出条数上限时回退到应用侧调度与本地通知，并保留源端的链式重挂（只发布最近一次发生时，在触发或回前台时补挂下一次）；回退与上限处理写进验收，按钮路由做不到时把相关验收标为阻塞，不只记 GAP。
5. 源端按钮经透明跳板 Activity 处理时，保留其拦截与前后台语义（应用在前台时的模态选择、取消或过去时刻的提示、离开时释放），不只在入口 onCreate/onNewWant 加一行分发。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-97530cfa88ec30cb186c](../../../store/cases/case-97530cfa88ec30cb186c/e9a66b9b0d513325b2858b3d811641c06df59f79e8673e56184c2c01be9d3376.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`e9a66b9b0d513325b2858b3d811641c06df59f79e8673e56184c2c01be9d3376`
