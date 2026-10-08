# “页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色

ID：`lesson-2e4279c4b82f06af64fd` · 版本：4 · 阶段：spec/execute · 主题：[ui/theme/tokens](index.md)

概要：“零硬编码色值”只禁字面值，允许 $r 引用语义色

信号：`$r('app.color`, `#RRGGBB`, `backgroundColor`, `fontColor`, `color.json`

## 何时使用

规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时

## 适用情境

规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。

## 原因

“零硬编码”的目的是把色值集中在 base/dark 资源里切换，$r('app.color.x') 引用恰好满足它。把它读成“不得设置颜色属性”，控件就退回平台默认色。来源中实现者已注意到按钮默认蓝与源端紫不同，却因这条约束放弃设置颜色。

## 做法

1. 规格写这类约束时同时写明“颜色一律用 $r('app.color.<语义名>') 引用已迁移资源”，并在需要颜色的控件行给出具体资源名。
2. 实现时遇到该约束，只避免 '#RRGGBB' 等字面色值，按源端语义把 backgroundColor、fontColor 等属性设为资源引用。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../sources/lesson-47785524c7f132ea7efe.lesson.md)（共享 1 张卡）
- [规格与源码冲突时按源端语义实现并标注差异](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-97a40a9d2dce65dc9f9c](../../../../../store/cases/case-97a40a9d2dce65dc9f9c/6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a.json) · 结论：diagnosis, rec-e47c290802, rec-e645901bde
  卡片版本：`6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a`
