# 把 remember 的「离开组合即销毁」写成复位方案时，规格列出框架会恢复的焦点等 UI 状态

审的是：规格
触发（任一种）：
- 读到：源页面状态用 remember {}（不是 rememberSaveable）持有，其中 focused 等字段由 onFocusChanged 这类框架事件驱动、直接决定显示分支；写错的样子：规格的复位方案只写「重新 new 状态对象」，把 TextInput.onFocus / onBlur 无条件映射到业务 focused，平台差异只写「Tabs / NavDestination 保活需主动复位」，验收「返回后 focused=false」只留 判:ui
适用范围：目标页面常驻在 Navigation 的 NavBar 或保活的 Tabs / Stack 里、会被 pushPath 覆盖再返回时，规格提取阶段写复位方案和验收条目
做法：
- 除数据字段外逐项列出目标框架会替用户恢复的 UI 状态（焦点、IME、滚动位置、选区），每项写明 ArkUI 侧的复位或判别手段（如焦点：判别 onFocus 来源，非用户触发的 stopEditing + clearFocus）
- 由框架事件驱动的业务字段，把「返回后为 false」写成可机械核对的验收步骤（push 子页 → 系统返回 → 核对 TextInput 未获焦、显示的分支），不只留 判:ui
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- NavBar、NavDestination 都是层级页面；层级页面非首次获焦时由上次获焦的节点获焦，Navigation 的路由切换属于整体获焦：子页 pop 后焦点回到 NavBar 上次获焦的 TextInput，onFocus 会再触发（出处：arkts-common-events-focus-event.md，基础概念 / 层级页面/容器整体获焦时的焦点链）
- push 子页再返回后 TextInput focused=true、键盘拉起，重新 new 的状态对象被 onFocus 写成 focused=true：只复位数据字段时观察到的行为（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c6aa20bd8974dabefc7b（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 2 ← 诊断
