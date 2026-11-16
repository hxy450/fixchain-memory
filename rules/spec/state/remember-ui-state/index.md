# remember 持有、由焦点等框架事件驱动的页面状态

agent 会看到什么：读到源页面状态用 remember {}（不是 rememberSaveable）持有，其中 focused 等字段由 onFocusChanged 这类框架事件驱动；规格的复位方案只写「重新 new 状态对象」，把 TextInput.onFocus / onBlur 无条件映射到业务 focused

## 规矩

- rule-2125a7c0fa4c｜把 remember 的「离开组合即销毁」写成复位方案时，规格列出框架会恢复的焦点等 UI 状态｜读到：源页面状态用 remember {}（不是 rememberSaveable）持有，其中 focused 等字段由 onFocusChanged 这类框架事件驱动、直接决定显示分支；写错：规格的复位方案只写「重新 new 状态对象」，把 TextInput.onFocus / onBlur 无条件映射到业务 focused，平台差异只写「Tabs / NavDestination 保活需主动复位」，验收「返回后 focused=false」只留 判:ui
