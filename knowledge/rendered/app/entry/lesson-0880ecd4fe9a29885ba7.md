# System.exit/killProcess 式“重启”迁为 ApplicationContext.restartApp，并携带系统原本重建的界面状态

## 何时使用

规格提取与入口实现阶段，为源端进程退出类调用（System.exit、Runtime.exit、Process.killProcess）确定目标行为与状态保留要求时（方法注释或调用点表明意图是重启）

## 适用情境

源方法注释或调用点表明意图是重启（语言切换、数据恢复或重置后、导入完成通知点击），实现只有 System.exit(0)；源前台进程被杀后，Android 按残留任务栈重建 Activity 并交回 savedInstanceState（抽屉开合、列表位置、搜索条件等）；目标在 UIAbility.terminateSelf 与 ApplicationContext.restartApp 之间选择。

## 例外与边界

- 调用点的用户可见终态就是离开应用（如“退出”菜单、上报后结束的致命错误处理），或调用时应用已在后台、没有前台任务可重建的，按退出处理，不改成 restartApp。

## 原因

System.exit 杀的是进程而不是任务：前台任务仍在时，系统拉起新进程按任务栈与保存态重建界面，用户看到的是“重启后回到原处”。按字面译成 terminateSelf 只会退出应用，调用点期望的重新进入主页与状态保持全部丢失；目标也不会替应用保存这些界面状态。

## 做法

1. 写契约前 grep 该方法的全部调用点并读方法注释，按调用点的用户可见终态（重启后进入主页、抽屉状态保持）定义行为；同一源方法在多份规格中口径不一时，以描述用户可见终态的条目为准统一服务层契约。
2. 目标用 ApplicationContext.restartApp(want) 拉起入口 Ability；源端靠 savedInstanceState 恢复的界面状态由应用写入 want 参数或持久化，并在冷启时读回；入口原有的验密等门控照常先行。
3. restartApp 在应用前台且窗口获焦后调用（例：windowStageEvent 进入 ACTIVE 之后；已观察到在 onForeground 中调用会因不在前台被拒绝），失败时退回 terminateSelf 并留下可观察的失败日志。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 2、3 步〕ApplicationContext.restartApp 重启应用并拉起自身指定的 UIAbility，重启时不触发 Ability 的 onDestroy；仅支持主线程调用，待重启的应用需要处于获焦状态
- 〔做法第 3 步〕restartApp 在 UIAbility 不在界面顶层时抛 16000053，目标不属于当前应用或不是 UIAbility 时抛 16000063，重启过于频繁时抛 16000064（至少隔 3 秒）
- 〔做法第 3 步〕WindowStageEventType.ACTIVE 表示窗口阶段获得焦点
- 〔原因〕UIAbilityContext.terminateSelf 只销毁当前 Ability，不重新拉起
- 〔适用情境 / 原因〕安卓 onSaveInstanceState 保存的 Bundle 在 Activity 重建时交给 onCreate 或 onRestoreInstanceState 恢复；应用没有覆写 onSaveInstanceState 时，默认实现保存窗口视图层级和 Fragment 状态
