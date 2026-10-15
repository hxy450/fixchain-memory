# 配置驱动的编辑项列表按源工厂表逐项分派：每个 type 接专属页面、按配置顺序在同一列表内渲染，未匹配类型空渲染；不压成通用控件、不移到列表外，也不用过滤条件静默去掉某类

ID：`lesson-71f8a80418dbc2c442ce` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与对齐阶段，为按配置（如 editorConfig）生成的编辑区确定每项的承载组件、顺序与间距，或增删列表的过滤条件时

## 适用情境

源端编辑 Fragment 遍历配置，经工厂把每一项（含外观类 bg/textColor/border 与 photo、text 等）各自创建为对应 Fragment，按顺序加入同一个无间距容器，未匹配类型落到空 Fragment；目标工程已有大量逐类型专页，另有页内文本编辑器、通用控件骨架或子模块选择等替代入口。

## 原因

压成通用控件，或把外观项、文本项移到列表外，会同时改变承载组件、顺序与间距，并产生重复入口；为与替代入口去重而写的 type 过滤，在替代入口被删除或更换后仍然生效，某类配置项就从列表里消失。

## 做法

1. 把源端工厂的 type→Fragment 表逐行落成显式分派：已有专页的类型直接接专页；需要页面级编辑器的外观类也通过同一列表插槽按配置顺序渲染，不在列表外提前放置。
2. 工厂的 else/空 Fragment 分支实现为空渲染，与“迁移未实现”区分：未匹配类型不显示占位文案，未接入的已知类型写进交付报告。
3. 列表容器和插槽不加统一间距：每项的上下间距取自其源 Fragment 根布局，公共容器只保留源端外壳的那一次间距。
4. 每个受支持的 type 按工厂进入列表且只有一个入口；改由目标已有入口承载某类时先记录决策，不用列表过滤静默替代。删除或替换替代入口时，同时移除列表提供函数里与该 type 相关的排除条件；接手已有通用骨架时先对照工厂表判断是扩展还是替换。

## 可选检查

- 为根文档写用例：配置为 [photo, text] 且未选子模块时，两项都在列表中、顺序与配置一致。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-625eea78c41ac46eb931](../../../store/cases/case-625eea78c41ac46eb931/e1c274485b319dc9bdac30bc37fe4c1f7fbab57367f176e25c6bc96213af2fcc.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e1c274485b319dc9bdac30bc37fe4c1f7fbab57367f176e25c6bc96213af2fcc`
- [case-6fc0687402faa0e4f9a5](../../../store/cases/case-6fc0687402faa0e4f9a5/fe8182ed8f96b2deb850f4297e64ca7c047b1792637a5bb905f2ec0176e065a4.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`fe8182ed8f96b2deb850f4297e64ca7c047b1792637a5bb905f2ec0176e065a4`
