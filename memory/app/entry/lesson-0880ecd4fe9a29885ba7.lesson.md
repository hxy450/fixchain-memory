# System.exit/killProcess 式“重启”迁为 ApplicationContext.restartApp，并携带系统原本重建的界面状态

ID：`lesson-0880ecd4fe9a29885ba7` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与入口实现阶段，为源端进程退出类调用（System.exit、Runtime.exit、Process.killProcess）确定目标行为与状态保留要求时

## 适用情境

源方法注释或调用点表明意图是重启（语言切换、数据恢复或重置后、导入完成通知点击），实现只有 System.exit(0)；源前台进程被杀后，Android 按残留任务栈重建 Activity 并交回 savedInstanceState（抽屉开合、列表位置、搜索条件等）；目标在 UIAbility.terminateSelf 与 ApplicationContext.restartApp 之间选择。

## 原因

System.exit 杀的是进程而不是任务：前台任务仍在时，系统拉起新进程按任务栈与保存态重建界面，用户看到的是“重启后回到原处”。按字面译成 terminateSelf 只会退出应用，调用点期望的重新进入主页与状态保持全部丢失；目标也不会替应用保存这些界面状态。

## 做法

1. 写契约前 grep 该方法的全部调用点并读方法注释，按调用点的用户可见终态（重启后进入主页、抽屉状态保持）定义行为；同一源方法在多份规格中口径不一时，以描述用户可见终态的条目为准统一服务层契约。
2. 目标用 ApplicationContext.restartApp(want) 拉起入口 Ability；源端靠 savedInstanceState 恢复的界面状态由应用写入 want 参数或持久化，并在冷启时读回；入口原有的验密等门控照常先行。
3. restartApp 在应用前台且窗口获焦后调用（例：windowStageEvent 进入 ACTIVE 之后；已观察到在 onForeground 中调用会因不在前台被拒绝），失败时退回 terminateSelf 并留下可观察的失败日志。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-29db923e9cadbe8ce53c](../../../store/cases/case-29db923e9cadbe8ce53c/aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761.json) · 结论：recommendation:3
  卡片版本：`aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761`
- [case-f85c825bb16d5a79901c](../../../store/cases/case-f85c825bb16d5a79901c/3b1b9007616b4e373f4e7b0c5200cd412af7e5a4336c4ddc52d6a4b465a5b552.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3b1b9007616b4e373f4e7b0c5200cd412af7e5a4336c4ddc52d6a4b465a5b552`
