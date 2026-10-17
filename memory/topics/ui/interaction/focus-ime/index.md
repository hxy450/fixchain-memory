# ui/interaction/focus-ime

焦点链与输入法：按键事件挂载点、可获焦组件、软键盘收放 API、首屏获焦时机与搜索框状态

[上一级](../index.md)

## 本级经验

- [Activity onKeyDown 挂页根，页内需可获焦](lesson-80e1d2c095a3698a7156.lesson.md) · 阶段：execute · 信号：onKeyDown, dispatchKeyEvent, onKeyEvent, NavDestination
- [SearchView 展开焦点提交收起分开建模](lesson-4995a3977dc8bc7fa696.lesson.md) · 阶段：spec/execute · 信号：SearchView, actionView, expandActionView, collapseActionView
- [收键盘用 hideTextInput，焦点绑 onFocus](lesson-99da84bf5c70367eb3df.lesson.md) · 阶段：execute · 信号：hideTextInput, showTextInput, hideSoftKeyboard, showSoftKeyboard
- [根快捷键只处理根上收过按下的抬起](lesson-a10cde3d336eee4eebe7.lesson.md) · 阶段：execute · 信号：onKeyUp, onKeyEvent, KeyType.Up, KeyType.Down
- [首屏输入框待窗口获焦后再 requestFocus](lesson-9d42548ee3c075de3330.lesson.md) · 阶段：execute · 信号：requestFocus, window.findWindow, isFocused, WINDOW_ACTIVE
