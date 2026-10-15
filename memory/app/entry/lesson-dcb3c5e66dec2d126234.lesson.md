# 源端首帧前按偏好设主题时，入口 onCreate 同步读偏好并在 loadContent 前 setColorMode，不用不等待的异步恢复

ID：`lesson-dcb3c5e66dec2d126234` · 版本：2

[本主题](index.md)

## 何时使用

入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时

## 适用情境

源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。

## 原因

ApplicationContext.setColorMode 是进程态，每次启动都要恢复；不等待的异步恢复与 loadContent、首帧之间没有声明的先后关系，可能在首帧之后才完成，界面先按系统深浅色绘制再切换。接线者只看到“请在 onCreate 调用”，按原样补调用点不会发现时序问题；源端把主题放在 super.onCreate 之前正是为了首帧生效，这一时机只留在设计参考里时下游收不到。

## 做法

1. 在 EntryAbility.onCreate 的同步路径用 preferences.getPreferencesSync 读取主题键（@ohos.data.preferences.d.ts；getPreferences 返回 Promise），并在 onWindowStageCreate 的 loadContent 之前完成 setColorMode。
2. 规格提取读入口 Activity.onCreate 时，把 super.onCreate/setContentView 之前的调用（如 setTheme）连同“首帧前生效”的时机写进功能契约，并指定目标承接位置。
3. 为启动恢复写移交时写明时序约束（如“首帧前同步生效”）；接线者看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只机械补调用点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
