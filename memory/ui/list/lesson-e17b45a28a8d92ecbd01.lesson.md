# 多类型 Adapter 承载的页面按全部 item 布局和 handleXxx 分支建区块：默认态、文案模板与附属子卡都来自绑定代码

ID：`lesson-e17b45a28a8d92ecbd01` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与返修重建阶段，把主体内容由 RecyclerView 多类型 Adapter 承载的 Android 页面转成 ArkUI 页面、确定各区块结构与背景层级时

## 适用情境

源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，首屏卡片、趋势图、网格等区块分散在 addItemType 登记的 item 布局与 handleXxx/convert 绑定里：默认选中态、setText 拼接的文案模板（如“平均温度X”“N天降温/M天升温”）、按条件 visibility 显示的附属子卡；UI 快照可能是合成的，item 布局清单可能为空。

## 原因

只凭区块标题或绑定代码片段推断卡片，会写出固定高度的占位列表、只有标题的卡片，把原始数值 toString 输出，还会删掉附属子卡；RecyclerView 本身无背景、叠在头图之上的层级也容易被一个不透明列表背景盖住。来源为同一应用的两次写入：生成期转换者读到 Adapter 有七类区块，却没打开任何 item 布局就写盘，内容列表背景遮住头图、15日区只有文字列表、40日区只有标题；返修重建者读到 handleForty/handleLife 后，仍把 40 日文案写成原始数值、删掉旧入口却没建黄历宜忌子卡。

## 做法

1. 从 addItemType/onCreateViewHolder 列出全部 item 布局并逐个读取，按 item 布局实现区块；规格提取时把这些 item 布局登记进页面规格的布局清单。
2. 逐个 handleXxx 抄录 setText 的文案模板和全部分支、visibility 控制的子卡、默认选中态；默认分支就是首屏形态，切换控件要真正切换渲染内容。删除旧骨架入口前，先找到它在源端对应的完整区块并用等价组件替换。
3. 源 RecyclerView 与根容器没有背景、头图在下层时，目标滚动内容层保持透明，只给各卡片设置自身背景。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-55bbad53c11b2d1b95e6](../../../store/cases/case-55bbad53c11b2d1b95e6/0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7`
- [case-5d12548f9d559985c27d](../../../store/cases/case-5d12548f9d559985c27d/608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0`
