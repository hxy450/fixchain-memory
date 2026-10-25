# Compose DropdownMenu、cascade 级联菜单与居中 Popup 菜单按源形态还原：锚定或居中、无变暗遮罩、子菜单在同一菜单内原地切层

ID：`lesson-b1006cf9981e5ff9bb2d` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-45230e39613edd881823](../../../store/cases/case-45230e39613edd881823/7949b6461d6df4d179e1766b8d90d9da28f6f5cd9816afaff2b4104f11ed15d7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`7949b6461d6df4d179e1766b8d90d9da28f6f5cd9816afaff2b4104f11ed15d7`
- [case-69c1c089176794fbe5db](../../../store/cases/case-69c1c089176794fbe5db/b6131de55c36c64007547c63dde577de0ce2d2dc6c6b56d93289e389777e5a27.json) · 结论：recommendation:3
  卡片版本：`b6131de55c36c64007547c63dde577de0ce2d2dc6c6b56d93289e389777e5a27`
