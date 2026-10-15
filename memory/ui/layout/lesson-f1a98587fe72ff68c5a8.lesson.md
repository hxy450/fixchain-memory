# 页面转换按源 XML 初始可见性与全部 setVisibility 决定节点是否渲染：gone 且从未设为可见的不生成，invisible 保留占位

ID：`lesson-f1a98587fe72ff68c5a8` · 版本：6

[本主题](index.md)

## 何时使用

页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构时；迁移标题栏或工具栏图标按钮、结果标题行等并决定是否显示时

## 适用情境

源布局含 visibility=gone/invisible 的标题、图标按钮或容器；Activity 对 gone 的图标 findViewById 并绑定点击，全文没有 setVisibility(VISIBLE)，或只改它子控件的文案与可见性、从不让容器本身可见；迁移用的页面快照可能是合成的，把 gone 节点列为可见文本或缺少 visibility 属性；目标工程其他页面已有同类入口的现成写法。

## 例外与边界

- 源端在不同状态分支里切换该节点的可见性时，按状态切换的显隐规则逐分支迁移

## 原因

点击监听只说明代码可达，不说明控件可见；照搬目标工程其他页面的入口惯例或合成快照，会把源端隐藏的入口生成为可见按钮。子控件的 setText、setVisibility 也不代表父容器会显示。invisible 不可见但仍占布局空间（View.java 对 INVISIBLE 的定义），gone 不占位。

## 做法

1. 以源布局 View id 为清单逐个决定是否生成节点：先看 XML 初始 visibility，再查代码中对该 View 及其父容器的全部 setVisibility；快照可见文本与源 XML 冲突时以源 XML 为准。
2. 只有 findViewById 与点击监听、没有 VISIBLE 分支的 gone 入口不生成；gone 容器从未被设为可见时不渲染（或 Visibility.None），即使代码改了它子控件的文案。
3. invisible 的节点写 Visibility.Hidden 保留占位（enums.d.ts：Hidden 参与布局占位，None 不占位），并核对隐藏期间子节点是否仍可交互。
4. 源端靠左右对称让中间控件居中时，隐藏一侧用与对侧控件同尺寸的空占位（尺寸取对侧控件的 layout_width/layout_height）保持居中，不放可点击图标。
5. 目标工程其他页面的写法只决定怎样实现，不决定源页是否有该入口；有截图时新增可见元素前用截图核对，协调者追加的入口要求与源布局或截图冲突时先回报冲突。
6. 转换前按页面状态（有数据、为空、结果、无结果）列出各自可见的标题与删除入口，确认同一语义只出现一次；目标代码里声明并在更新函数中赋值的展示状态，要在 build 中有消费它的组件。

来源支持：4 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-436d1b16d79796c667d6](../../../store/cases/case-436d1b16d79796c667d6/fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70.json) · 结论：diagnosis, recommendation:4
  卡片版本：`fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70`
- [case-5b7b00a1deb25ed0b8d3](../../../store/cases/case-5b7b00a1deb25ed0b8d3/919bf87f71df8c5347bde16fb06fa3396a51d284ab648ce5d123265dfbf05b5e.json) · 结论：recommendation:1
  卡片版本：`919bf87f71df8c5347bde16fb06fa3396a51d284ab648ce5d123265dfbf05b5e`
- [case-a348083ad18c6f87030f](../../../store/cases/case-a348083ad18c6f87030f/ff4ca14c213bc58cab29a246315afb07ff950c3ead8d54b4816a9b98629adda5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`ff4ca14c213bc58cab29a246315afb07ff950c3ead8d54b4816a9b98629adda5`
- [case-be590c45de6e4195a7aa](../../../store/cases/case-be590c45de6e4195a7aa/8bd4ff591319a27aad91736ee43fe1cde1fd581f63d209f68e730ac2f406e5bb.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`8bd4ff591319a27aad91736ee43fe1cde1fd581f63d209f68e730ac2f406e5bb`
