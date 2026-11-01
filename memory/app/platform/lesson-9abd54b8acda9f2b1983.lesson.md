# 源端 await 分享结果再提示时，systemShare 的 show() 只代表面板已拉起：按 shareCompleted/dismiss 结算成功与取消

ID：`lesson-9abd54b8acda9f2b1983` · 版本：2

[本主题](index.md)

## 何时使用

平台能力实现阶段，把源端会等待用户结果的分享调用映射为目标 API，并安排其后的成功/失败提示时

## 适用情境

源代码先 await 插件的分享调用（如 Capacitor Share.share），之后弹成功提示、catch 中弹失败提示；目标用 HarmonyOS systemShare.ShareController，show() 返回 Promise<void>，另有 on('shareCompleted') 与 on('dismiss') 事件。

## 原因

源插件的 Promise 在用户完成或取消后才结算（@capacitor/share 的 Android 实现在选择器返回 RESULT_CANCELED 时 reject "Share canceled"），目标 show() 在面板拉起后就 resolve；直接 await show() 会在面板还开着时弹成功提示，用户取消也没有任何失败反馈。

## 做法

1. 映射前分别核实两端 Promise 何时结算、取消时 resolve 还是 reject：源端以插件原生实现为准，目标以 d.ts 或官方文档为准；时机不同就不能直接用 await 替换。
2. 目标把用户结果拆成事件时，在 show 前注册监听并包成 Promise：shareCompleted → resolve，未完成就 dismiss → 按源取消原因 reject，show() 失败 → reject；用标志保证只结算一次，结算后 off 两个监听，让调用方原有的成功/失败提示落在真正的终态之后。
3. 写前已发现“取消时 resolve 还是 reject 无法确认”这类疑点时，读源插件与目标文档消除；做不到就记入 decision_gaps，不在注释里写“同语义”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-096c031832b60ef8b78e](../../../store/cases/case-096c031832b60ef8b78e/967cefb2a48ad79bfbe217ca3d6a41739ab2037b412ffb6cc25fb1e06066bf03.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`967cefb2a48ad79bfbe217ca3d6a41739ab2037b412ffb6cc25fb1e06066bf03`
