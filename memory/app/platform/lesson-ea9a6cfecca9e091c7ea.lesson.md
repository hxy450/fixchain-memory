# 源端靠窗口销毁或会话结束自动解除的常亮、安全标志与画中画态，迁到共享主窗口或应用自管状态后按拥有者成对复位

ID：`lesson-ea9a6cfecca9e091c7ea` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与页面实现阶段，把 Activity 窗口标志、WakeLock 或画中画映射为鸿蒙窗口 API 与应用内状态并写验收时；实现计时等会话的后台交接、完成与停止路径时

## 适用情境

源端某个 Activity 在 onCreate 给 getWindow() 加标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）且没有清除代码，靠该 Activity 不可见或 finish 时随窗口失效；或计时等会话持有 WakeLock、进入系统画中画，随会话结束或退出画中画由系统复位。目标各页以 Navigation/NavDestination 共用一个主窗口，用 setWindowKeepScreenOn、setWindowPrivacyMode 等窗口级 API，或用应用内紧凑模式代替画中画，复位要自己写。

## 例外与边界

- 源端已在 onPause/onStop 或会话结束处显式 clearFlags、release 时，按其代码位置映射

## 原因

目标主窗口全应用共享，窗口级设置一直生效到显式改回；应用内紧凑模式等自管状态也不会随系统事件自动退出。只在进入时打开、漏掉任一退出路径，离开页面或会话结束后效果仍残留；验收只测“进入后生效”时发现不了。

## 做法

1. 先按源端写法确定拥有者与作用范围：加在某个 Activity 自身窗口上的标志，作用范围是该页面可见期间；会话持有的常亮（代替 WakeLock 或会话开启的 FLAG_KEEP_SCREEN_ON）与紧凑模式，作用范围是该会话。
2. 页面拥有的标志写成成对开关：NavDestination onShown 设 true、onHidden 设 false（仍受源端读取的偏好约束），不写“onCreate 时机设 true”。窗口对象经工程主窗口入口取（windowStage.getMainWindowSync() 或已封装的主窗口获取函数），不用 window.getLastWindow：它返回当前应用最上层的窗口，有子窗口时不是主窗口（@ohos.window.d.ts）。
3. 会话拥有的状态按状态分列退出点：常亮在后台交接、后台完成、通知停止与页面销毁时复位，回前台时会话仍在就不关闭；紧凑模式在回前台、后台完成与通知停止时退出。检索每处置为 true 的位置，核对每条退出路径都有对应的 false。
4. 跨栈基线表的窗口级映射行注明“目标窗口全应用共享，须随拥有者成对开关”；设备判据补离开一侧（返回主菜单后按系统超时熄屏，可用 hidumper 查本应用窗口锁已释放）。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-42fb1284b2edc857b78b](../../../store/cases/case-42fb1284b2edc857b78b/1ec9ca3305bf0aaf2592d3df82c58adfa8db844dc2f0f12c41ad008281976b71.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`1ec9ca3305bf0aaf2592d3df82c58adfa8db844dc2f0f12c41ad008281976b71`
- [case-e92bb15630afd5b03216](../../../store/cases/case-e92bb15630afd5b03216/3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c.json) · 结论：recommendation:4, recommendation:5
  卡片版本：`3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c`
