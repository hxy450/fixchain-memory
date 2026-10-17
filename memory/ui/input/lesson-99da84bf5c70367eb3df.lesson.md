# 收软键盘用 hideTextInput，不用 hideSoftKeyboard 或 stopInputSession；焦点态绑 onFocus/onBlur

ID：`lesson-99da84bf5c70367eb3df` · 版本：1

[本主题](index.md)

## 何时使用

界面与服务实现阶段，为搜索框等输入框实现“展开取焦、提交收键盘、菜单随焦点切换”并选择输入法控制 API 时

## 适用情境

源端用 InputMethodManager.hideSoftInputFromWindow/showSoftInput 只收放键盘、焦点不变，或由 SearchView 焦点变化驱动菜单与工具栏；规格写“输入法方法实现期核实后钉死”；目标准备调用 showSoftKeyboard/hideSoftKeyboard、stopInputSession，或用点击时手工翻转的布尔量表示“输入框已聚焦”。

## 原因

inputMethodController 各方法的权限与副作用不同：showSoftKeyboard/hideSoftKeyboard 声明需要 ohos.permission.CONNECT_IME_ABILITY，三方应用调用被拒；stopInputSession 结束输入会话并使编辑框失焦；hideTextInput 只收起键盘。手工布尔量不随系统焦点变化更新，菜单状态与源端分叉。

## 做法

1. 写调用前在 SDK 的 @ohos.inputMethod.d.ts 核对所选方法的 @permission 与说明：只收键盘用 inputMethod.getController().hideTextInput()，拉起用 showTextInput()；核对无结果时继续查声明，不用 catch 吞掉被拒错误。
2. 规格把菜单或工具栏状态挂在输入框焦点上时，状态由 TextInput 的 onFocus/onBlur 写入；展开时经 focusControl.requestFocus 取焦，输入框按条件构建时先置待取焦标记，在它的 onAppear 之后再取焦。
3. 收键盘的调用方依赖焦点态时，把“收键盘引发的失焦”单独标记，不让它进入焦点变化分支。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-384517eb6b32c1c41f94](../../../store/cases/case-384517eb6b32c1c41f94/f6b049b4e7d9d6b5843e5cbe8da445a3fbc85ed7c0ac24b67adbcfc775926baa.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f6b049b4e7d9d6b5843e5cbe8da445a3fbc85ed7c0ac24b67adbcfc775926baa`
