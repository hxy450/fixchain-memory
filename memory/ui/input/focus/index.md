# ui/input/focus

Navigation 返回后的焦点恢复与 TextInput 业务状态

[上一级](../index.md)

## 本级经验

- [常驻 NavBar 页面的 TextInput.onFocus 不能 1:1 当作用户聚焦：先判别焦点来源再写业务状态](lesson-034ff7e39ef05820dd53.lesson.md)
  - 时机：界面实现阶段，把 TextInput 的焦点回调接到页面业务状态、且页面处于 Navigation NavBar / 常驻 Stack 会被 pushPath 覆盖时
  - 情境：页面用 focused 之类业务字段决定显示分支（Suggestions vs Categories）；从子页系统返回后 ArkUI 会把焦点交还该 TextInput。
- [翻译「离开组合即销毁」的 remember 状态时，逐项列出目标框架会替用户恢复的 UI 状态（焦点、IME 等）](lesson-0b0c476cdbcc543a88fa.lesson.md)
  - 时机：规格提取阶段，把源端 remember（非 rememberSaveable）随组合销毁的状态语义翻译成目标端复位方案时
  - 情境：源页面靠 remember 在离开组合时丢弃全部状态，其中 focused 等由框架事件驱动的字段直接决定显示分支；目标端该页面常驻在 Navigation 的 NavBar（Stack/Tabs 保活）中，经 pushPath 进入子页后再系统返回。
