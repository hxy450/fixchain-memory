# 只收键盘不清焦点用 hideTextInput：show/hideSoftKeyboard 需系统权限，stopInputSession 会让输入框失焦

## 何时使用

界面与服务实现阶段，把 InputMethodManager 的显示、隐藏软键盘调用迁到 IMEKit 或 ArkUI 输入组件时

## 适用情境

源端用 InputMethodManager.hideSoftInputFromWindow 只收键盘、焦点仍留在输入框，或用 showSoftInput 弹键盘；规格写“inputMethodController，具体方法实现期核实”；目标是三方应用，调用方可能依赖输入框的焦点态。

## 例外与边界

- 源端收键盘时同时 clearFocus：此时结束编辑并失焦正是源端语义

## 原因

@ohos.inputMethod 的 InputMethodController 中几组方法副作用不同：showSoftKeyboard/hideSoftKeyboard 需要系统权限 ohos.permission.CONNECT_IME_ABILITY，三方应用调用被拒，catch 吞掉后键盘不受控；stopInputSession 结束输入会话并使编辑框失焦，依赖焦点的工具栏状态随之翻转；hideTextInput 只隐藏键盘。

## 做法

1. 写前在 SDK 的 @ohos.inputMethod.d.ts 核对所选方法的 @permission、@systemapi 与对焦点和会话的影响；只收键盘、保留焦点用 hideTextInput()（它和 showTextInput 要配对使用：收起后需要再输入时，先调 showTextInput 重新进入编辑状态；输入框仍在焦点上，不会再经获焦拉起键盘），弹出用 showTextInput() 或让 TextInput 自身获焦拉起；源端同时清焦点时才用 stopInputSession。
2. 规格要求“实现期核实”而检索无结果时，继续查 d.ts 声明，不用 catch 吞掉调用失败收口；失败分支打日志，保持可观察。

## 可选检查

- 有设备时收起键盘后看焦点回调或 hilog，确认输入框仍处于聚焦。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕安卓 InputMethodManager.hideSoftInputFromWindow 从当前接收输入的窗口请求隐藏软键盘，本身不清除视图焦点
- 〔原因 / 做法第 1 步〕InputMethodController.hideSoftKeyboard、showSoftKeyboard 需要 ohos.permission.CONNECT_IME_ABILITY，仅系统应用可用，三方应用调用时以 201（权限校验失败）报错
- 〔原因 / 做法第 1 步〕文档写明 InputMethodController.stopInputSession 结束当前输入会话并隐藏软键盘；hideTextInput 隐藏软键盘、让编辑框退出编辑状态，但不解除与输入法的绑定，之后要先调 showTextInput 才能再进入编辑状态
- 〔原因 / 做法第 1 步〕设备上调 stopInputSession 后编辑框失焦（hilog 可见），调 hideTextInput 只收起键盘
- 〔做法第 1 步〕InputMethodController.showTextInput 在编辑框没有获焦、或当前没有编辑框绑定输入法时抛 12800003
