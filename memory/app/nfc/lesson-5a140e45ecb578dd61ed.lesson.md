# NFC 能力前置检查按源端三分支迁移：不支持、已关闭（打开系统 NFC 设置）、可用分别建模，不用一个布尔可用门折叠

ID：`lesson-5a140e45ecb578dd61ed` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与服务、ViewModel 实现阶段，把源端读卡入口前的 NFC 能力检查转写为服务接口、状态枚举、提示文案与验收条款时

## 适用情境

Android 入口先判 NfcAdapter 是否为 null（设备不支持，提示后不导航），再判 isEnabled()（开关关闭时跳 Settings.ACTION_NFC_SETTINGS，返回后需再次点击），都通过才进入读卡；目标以 HarmonyOS 的 canIUse 系统能力与 nfcController 开关状态实现；用来取证的设备可能只覆盖其中一种结果（如测试机不支持 NFC）。

## 原因

“不可用”是多个源分支的并集：开关关闭时源端引导用户去系统设置打开，而不是提示设备不支持。服务层只给一个 isAvailable() 布尔门、状态枚举没有关闭态时，下游只能把关闭并入不支持，支持 NFC 的设备会显示“不支持”且无法引导开启；真机证据只覆盖一种结果时，规格容易按观察面裁掉其余分支。

## 做法

1. 规格按源码分支逐一写服务接口、状态与验收：不支持 → 原提示且不导航；已关闭 → 打开系统 NFC 设置页并提示返回后再试；可用 → 进入读卡。标注“源:某函数()”的条款对照该函数全部 if/else 写全；设备只观察到部分分支时，其余仍按源码契约保留。
2. 服务层拆成可区分的结果（如 isSupported() 与开关状态、openSettings()，或返回 unsupported/disabled/available），调用异常单独处理；ViewModel 为每种结果设独立状态与反馈，不复用“不支持”文案。
3. 关闭分支用目标 SDK 的设置页接口实现（来源在 API 24 用 settings.openNfcSettingsPage）；实现时发现规格缺这一分支，按源码实现或作为阻塞缺口写进回执交裁决，不并入相邻分支。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3393a7b63a1c499d3e05](../../../store/cases/case-3393a7b63a1c499d3e05/087ad61eaf4cd66f5dd27160d6f41eb70eb9c6fde92f045fd1fa60037f6c32c9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`087ad61eaf4cd66f5dd27160d6f41eb70eb9c6fde92f045fd1fa60037f6c32c9`
