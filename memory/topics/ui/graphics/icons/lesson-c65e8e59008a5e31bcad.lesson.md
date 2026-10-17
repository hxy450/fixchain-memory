# 源端按使用场景返回不同资源变体时，按取值字段分别映射，不用一个映射覆盖所有场景

ID：`lesson-c65e8e59008a5e31bcad` · 版本：3 · 阶段：execute/repair · 主题：[ui/graphics/icons](index.md)

概要：编码到资源的多变体映射按取值字段拆分不合一

信号：`iconEx`, `bgEx`, `icon2Ex`, `setBackgroundResource`, `$r`, `webp`

## 何时使用

界面实现与返修阶段，把源端“编码 → 资源”的映射函数（如天气编码到图标）迁移为 $r 资源映射，并为各使用处选择资源时

## 适用情境

源端一个编码对应多种资源（白色图标、背景图、另一色系图标等），经 iconEx/bgEx/icon2Ex 一类字段分别取用，页面不同位置（顶部、小时卡、选中/非选中、列表）绑定不同字段。 也包括同一编辑选项在选择列表与主预览取自不同资源族：列表 Holder 用固定 drawable（setBackgroundResource），主预览按组件尺寸加载 cover/<尺寸>/<id>.webp。

## 原因

合并成单一映射会把背景图当小图标用，或让本应另一色系的列表图标都变成同一种。来源中执行者把天气图标映射到背景图；返修者读到源端分场景取用，仍把所有场景映射到白色图标，直到用户要求“白色云换成蓝色”。

## 做法

1. 按源端取值字段拆分映射函数（图标、背景、第二套图标各一个），在每个使用处按源端绑定的字段选择。
2. 按尺寸等条件选资源的规则，只落到源端实际按该条件加载的那一层（如主预览），不扩展到列表缩略图。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [编译修复只改报错行，不删功能或换异义替代](../../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [图标按资源固有 dp 显示，触摸盒放外层不设成盒尺寸](lesson-bdc493f5950835f9bfcc.lesson.md)（共享 1 张卡）
- [无来源兜底预览不加源端没有的边框选中态装饰](../images/lesson-c8909c3cb5f925913407.lesson.md)（共享 1 张卡）
- [折线点与标签共用原点，点坐标含留白时不再加 position](../drawing/lesson-dca31bed776aaf7cb328.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-9d7fa754a567e2ecec7e](../../../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：diagnosis, rec-9c783f4c4b
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-be863418bbabb4c9591a](../../../../../store/cases/case-be863418bbabb4c9591a/a182d6f5e595aa6593e53fc4f1afece909105dfa2d6df1c853072731743d3eef.json) · 结论：diagnosis, rec-41deb74cf4
  卡片版本：`a182d6f5e595aa6593e53fc4f1afece909105dfa2d6df1c853072731743d3eef`
