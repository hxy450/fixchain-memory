# 只收键盘不清焦点用 hideTextInput：show/hideSoftKeyboard 需系统权限，stopInputSession 会让输入框失焦

ID：`lesson-edae4e2795ec169255bb` · 版本：1

[本主题](index.md)

## 何时使用

界面与服务实现阶段，把 InputMethodManager 的显示、隐藏软键盘调用迁到 IMEKit 或 ArkUI 输入组件时

## 适用情境

源端用 InputMethodManager.hideSoftInputFromWindow 只收键盘、焦点仍留在输入框，或用 showSoftInput 弹键盘；规格写“inputMethodController，具体方法实现期核实”；目标是三方应用，调用方可能依赖输入框的焦点态。

## 例外与边界

- 源端收键盘时同时 clearFocus：此时结束编辑并失焦正是源端语义

## 原因

@ohos.inputMethod 的 InputMethodController 中几组方法副作用不同：showSoftKeyboard/hideSoftKeyboard 需要系统权限 ohos.permission.CONNECT_IME_ABILITY，三方应用调用被拒，catch 吞掉后键盘不受控；stopInputSession 结束输入会话并使编辑框失焦，依赖焦点的工具栏状态随之翻转；hideTextInput 只隐藏键盘。

## 做法

1. 写前在 SDK 的 @ohos.inputMethod.d.ts 核对所选方法的 @permission、@systemapi 与对焦点和会话的影响；只收键盘、保留焦点用 hideTextInput()，弹出用 showTextInput() 或让 TextInput 自身获焦拉起；源端同时清焦点时才用 stopInputSession。
2. 规格要求“实现期核实”而检索无结果时，继续查 d.ts 声明，不用 catch 吞掉调用失败收口；失败分支打日志，保持可观察。

## 可选检查

- 有设备时收起键盘后看焦点回调或 hilog，确认输入框仍处于聚焦。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-384517eb6b32c1c41f94](../../../../store/cases/case-384517eb6b32c1c41f94/f6b049b4e7d9d6b5843e5cbe8da445a3fbc85ed7c0ac24b67adbcfc775926baa.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f6b049b4e7d9d6b5843e5cbe8da445a3fbc85ed7c0ac24b67adbcfc775926baa`
