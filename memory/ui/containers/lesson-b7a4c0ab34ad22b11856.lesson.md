# DrawerLayout换成SideBarContainer时补齐源容器的默认行为

ID：`lesson-b7a4c0ab34ad22b11856` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把DrawerLayout抽屉页转成ArkUI SideBarContainer并设置侧栏宽度、分隔线、内容对齐与遮罩时；规格阶段声称两者语义对齐时同样适用

## 适用情境

源根布局为DrawerLayout，抽屉是wrap_content宽的ScrollView；目标用SideBarContainer(Overlay)加Scroll。

## 原因

两种容器默认值不同：DrawerLayout无分隔线，打开时画0x99000000遮罩，点遮罩收起且不把点击交给内容，ScrollView内容自顶部排；SideBarContainer默认带分隔线，Overlay模式无遮罩，Scroll内容不足一屏时居中。只换容器，外观和点击都会偏离。

## 做法

1. 显式设divider(null)、Scroll.align(Alignment.Top)；内容区上叠一层#99000000遮罩，随侧栏显隐切换，关闭时HitTestMode.None，点遮罩收起侧栏并消费这次点击。
2. 侧栏宽度按wrap_content计算：子项先按资源目录换算成vp，再取最宽者加margin。
3. 规格做容器映射时，把源容器的隐式默认（遮罩、点外部收起、分隔线、内容起排方向）列为实现验收点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-540ecdd38de3165e5d03](../../../store/cases/case-540ecdd38de3165e5d03/d1680892d4afde0858648aad9063ffbdea116cd79fb3574578d3ca210626908d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`d1680892d4afde0858648aad9063ffbdea116cd79fb3574578d3ca210626908d`
