# RecyclerView Adapter 承载的列表或页面，按每类 viewType 实际 inflate 的 item 布局与绑定建区块和外观

ID：`lesson-e17b45a28a8d92ecbd01` · 版本：3

[本主题](index.md)

## 何时使用

界面实现与返修重建阶段，把主体由 RecyclerView（尤其多类型 Adapter）承载的 Android 页面或列表转成 ArkUI，确定各区块结构、卡片背景圆角与背景层级时；参照兄弟页面卡片实现时；规格准备阶段为列表页登记 item 布局时

## 适用情境

源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，或 RecyclerView 用 tools:listitem 引用 item 布局；区块与行分散在 addItemType/onCreateViewHolder inflate 的各类 item 布局与 convert/bind 绑定里：默认选中态、setText 拼接的文案模板、按条件 visibility 显示的附属子卡。某类 holder 在绑定时 addView/inflate 子视图（如根视图为 CardView、带 cardCornerRadius），另一类有自己的背景 drawable。UI 快照可能是合成的，item 布局清单可能为空或只登记了一类。

## 原因

只凭区块标题、绑定片段或一类 item 布局推断，会写出占位列表、只有标题的卡片，把原始数值直接输出，删掉附属子卡，或把某一类的圆角与描边套到所有分支。RecyclerView 本身无背景、叠在头图之上的层级也容易被不透明列表背景盖住。兄弟页面的卡片 Builder 也是迁移产物，其数值不能当源端真值。

## 做法

1. 从 getItemViewType/addItemType/onCreateViewHolder 列出全部 item 布局并逐个读取，按 item 布局实现区块与行，取图标、文字层级与右侧列；RecyclerView 的 tools:listitem 指向的布局也要打开读取，结构以适配器实际 inflate 的布局为准。
2. holder 把动态视图 addView 到内容容器时，继续打开该视图的布局取背景、圆角与描边（如 cardCornerRadius 引用的 dimen 值）；只属于某一类的背景 drawable 只用在该类分支，共用 Builder 按 holder 类型取外观参数。
3. 逐个绑定方法抄录 setText 的文案模板和全部分支、visibility 控制的子卡、默认选中态；默认分支就是首屏形态，切换控件要真正切换渲染内容。删除旧骨架入口前，先找到它在源端对应的完整区块并用等价组件替换。
4. 源 RecyclerView 与根容器没有背景、头图在下层时，目标滚动内容层保持透明，只给各卡片设置自身背景。
5. 参照兄弟页面的卡片实现时只借结构，圆角、描边、底色逐项回到本页源码核对。规格准备阶段把各类 item 布局及其动态 inflate 的布局都登记进页面规格的布局清单。

来源支持：4 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-436d1b16d79796c667d6](../../../store/cases/case-436d1b16d79796c667d6/fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70.json) · 结论：recommendation:4
  卡片版本：`fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70`
- [case-55bbad53c11b2d1b95e6](../../../store/cases/case-55bbad53c11b2d1b95e6/0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7`
- [case-5b1b0e2ce03be0dc6d37](../../../store/cases/case-5b1b0e2ce03be0dc6d37/c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48`
- [case-5d12548f9d559985c27d](../../../store/cases/case-5d12548f9d559985c27d/608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0`
