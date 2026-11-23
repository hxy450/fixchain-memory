# Compose DropdownMenu、cascade 级联菜单与居中 Popup 菜单按源形态还原：锚定或居中、无变暗遮罩、子菜单在同一菜单内原地切层

## 何时使用

规格映射与界面实现阶段，为 Compose 下拉菜单、级联子菜单、居中操作菜单与偏好行的下拉菜单确定弹出形态时

## 适用情境

源端用 Material3 DropdownMenu、me.saket.cascade CascadeDropdownMenu、基于 Popup 的居中级联菜单或 compose-preference 的 DROPDOWN_MENU：菜单放在触发按钮所在 Box 内锚定弹出或屏幕居中弹出，不带变暗遮罩，点外与返回关闭，带 children 的项在同一菜单内切换到子层并有返回 Header；目标用 bindMenu 或自绘层。

## 原因

把它们写成灰遮罩自绘浮层、固定 top/right 面板、并排多列或平铺列表，会同时改变锚点、遮罩、关闭方式与层级切换；“ArkUI 不支持级联”的未验证判断和“形态差异由视觉断言容忍”的规格条款会放行这些偏离，后写的页面再把首个浮层当作项目先例复制。

## 做法

1. 规格把弹出形态写成可验收契约：锚点（菜单顶接触发按钮底，起点或末端对齐）、无遮罩、点外与返回关闭、children 原地切层并带返回 Header；居中级联写全屏透明层与宽度规则。不以“视觉断言容忍”放行锚点或遮罩差异；写“不支持级联/子菜单”前先查组件文档或做最小验证。
2. 实现优先用 bindMenu 锚定到触发按钮；必须自绘点外关闭层时保持透明，面板跟随各自锚点；偏好行的 DROPDOWN_MENU 锚在该行上弹出，不改成行内展开列表。
3. cascade 子菜单在同一容器内原地替换当前层（前进、返回与 Header），不并排多列，也不把 children 平铺成同级项。
4. 用 bindMenu 自定义内容承载级联时，轻点自定义内容会关闭菜单（来源修复期设备实测）：在子菜单入口与 Header 上截断触摸冒泡（如 onTouch 中 stopPropagation），点击手势照常响应。
5. 复用工程已有菜单写法前，对照本页 Android 源的菜单组件类型与遮罩、锚点语义，与源码不一致的先例不复制。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、2 步〕bindMenu 的菜单选项（ContextMenuOptions）没写 placement 时取 Placement.BottomLeft
- 〔做法第 1、2 步〕ContextMenuOptions.mask（API 20 起）没写时：有预览时为 true，否则为 false，即普通 bindMenu 菜单默认不带遮罩
- 〔做法第 1、3 步〕MenuItemOptions.builder 用于创建子菜单；Menu 的 subMenuExpandingMode 没写时为 SIDE_EXPAND（子菜单在同一平面侧边展开），EMBEDDED_EXPAND 嵌在主菜单内展开，STACK_EXPAND 浮在主菜单上方展开（API 12 起）
- 〔做法第 4 步〕bindMenu 以自定义 builder 作菜单内容时，轻点菜单里的自定义内容会关闭菜单
