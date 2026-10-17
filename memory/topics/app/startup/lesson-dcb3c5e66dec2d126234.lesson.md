# 源端在入口 onCreate 首帧前按偏好设主题时，目标在 EntryAbility.onCreate 同步读取偏好并在 loadContent 前 setColorMode；恢复函数返回 Promise 而调用方不等待，就是首帧后才生效

ID：`lesson-dcb3c5e66dec2d126234` · 版本：2 · 阶段：spec/execute · 主题：[app/startup](index.md)

概要：持久化主题在 loadContent 前同步设好

信号：`ApplicationContext.setColorMode`, `setColorMode`, `getPreferencesSync`, `loadContent`, `onWindowStageCreate`, `EntryAbility.onCreate`, `setTheme`, `super.onCreate`, `DayNight`, `HANDOFF`

## 何时使用

入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时

## 适用情境

源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。

## 原因

不等待的异步恢复在 loadContent 之后才完成，首帧先按系统深浅色绘制再切换；接线者只看到“请在 onCreate 调用”，按原样补调用点不会发现时序问题。源端把主题放在 super.onCreate 之前正是为了首帧生效，这一时机若只留在设计参考里、没写进功能契约，下游就收不到。来源中偏好 worker 自己注意到 setColorMode 是进程态、需跨启动恢复，仍写成 async 恢复并交接，收口者不等待地调用。

## 做法

1. 在 EntryAbility.onCreate 的同步路径用 preferences.getPreferencesSync 读取主题键，并在 onWindowStageCreate 的 loadContent 之前完成 setColorMode。
2. 规格提取读入口 Activity.onCreate 时，把 super.onCreate/setContentView 之前的调用（如 setTheme）连同“首帧前生效”的时机写进功能契约，并指定目标承接位置。
3. 为启动恢复写移交时写明时序约束（如“首帧前同步生效”）；接线者看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只机械补调用点。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [权限按目标 API 的 @permission 汇总](../capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md)（共享 1 张卡）
- [manifest 未声明的窗口缺省解析成目标值并指派](../entry/lesson-c1d7ec16bb02aa152c33.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-cc22f6cc1041c8cc1129](../../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：diagnosis, rec-77d8069e64, rec-d9808d4eae, rec-0af42a8bd7
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
