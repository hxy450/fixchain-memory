# 源端 await 分享结果再提示时，systemShare 的 show() 只代表面板已拉起：按 shareCompleted/dismiss 结算成功与取消

## 何时使用

平台能力实现阶段，把源端会等待用户结果的分享调用映射为目标 API，并安排其后的成功/失败提示时

## 适用情境

源代码先 await 插件的分享调用（如 Capacitor Share.share），之后弹成功提示、catch 中弹失败提示；目标用 HarmonyOS systemShare.ShareController，show() 返回 Promise<void>，另有 on('shareCompleted') 与 on('dismiss') 事件。

## 例外与边界

- on('shareCompleted') 从 API 18 起才有（show() 与 on('dismiss') 从 API 11 起）；工程兼容的最低版本低于 API 18 时只拿得到面板关闭，区分不了完成和取消，此时照第 3 步把这一差异记为缺口，不把 dismiss 当作分享成功。

## 原因

源插件的 Promise 在用户完成或取消后才结算（@capacitor/share 的 Android 实现在选择器返回 RESULT_CANCELED 时 reject "Share canceled"），目标 show() 在面板拉起后就 resolve；直接 await show() 会在面板还开着时弹成功提示，用户取消也没有任何失败反馈。

## 做法

1. 映射前分别核实两端 Promise 何时结算、取消时 resolve 还是 reject：源端以插件原生实现为准，目标以 d.ts 或官方文档为准；时机不同就不能直接用 await 替换。
2. 目标把用户结果拆成事件时，在 show 前注册监听并包成 Promise：shareCompleted → resolve，未完成就 dismiss → 按源取消原因 reject，show() 失败 → reject；用标志保证只结算一次，结算后 off 两个监听，让调用方原有的成功/失败提示落在真正的终态之后。
3. 写前已发现“取消时 resolve 还是 reject 无法确认”这类疑点时，读源插件与目标文档消除；做不到就记入 decision_gaps，不在注释里写“同语义”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕ShareController.on('shareCompleted') 在分享操作完成时回调（API 18 起）；on('dismiss') 在系统分享面板关闭时回调
- 〔原因〕await ShareController.show() 在系统分享面板刚拉起时就返回：紧跟其后弹出的成功提示被仍在显示的模态面板挡住；用户取消分享时 await 之后的失败分支不会出现
