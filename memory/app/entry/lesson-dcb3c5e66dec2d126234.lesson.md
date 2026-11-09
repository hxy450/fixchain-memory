# 源端首帧前恢复主题时显式建立完成顺序：未等待 Promise 不保证首帧前生效，setColorMode 调用时机按目标 SDK 核验

ID：`lesson-dcb3c5e66dec2d126234` · 版本：2

[本主题](index.md)

## 何时使用

入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时

## 适用情境

源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。

## 原因

不等待的异步恢复没有建立“恢复完成先于首帧”的保证；来源中确实在加载后才完成并切换，但不能据未等待本身断言每次必然晚于首帧。接线者只看到“请在 onCreate 调用”，按原样补调用点不会发现时序问题。源端把主题放在 super.onCreate 之前正是为了首帧生效，这一时机若只留在设计参考里、没写进功能契约，下游就收不到。来源中偏好 worker 自己注意到 setColorMode 是进程态、需跨启动恢复，仍写成 async 恢复并交接，收口者不等待地调用。

## 做法

1. 可先在同步路径读取主题偏好，但实际设置路径必须按目标 SDK 的调用前提核验。本轮官方 ApplicationContext.setColorMode 要求窗口已创建且页面 loadContent 已完成；不无版本依据地规定其必须在 loadContent 前调用。需要首帧即正确主题时，另核该版本支持的启动配置与主题方案，未证实的路径保留具体缺口，不能仅以调用点已补就验收。
2. 规格提取读入口 Activity.onCreate 时，把 super.onCreate/setContentView 之前的调用（如 setTheme）连同“首帧前生效”的时机写进功能契约，并指定目标承接位置。
3. 为启动恢复写移交时写明时序约束（如“首帧前同步生效”）；接线者看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只机械补调用点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
