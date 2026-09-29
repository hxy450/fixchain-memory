# ConstraintLayout 中单视图对 parent 居中、兄弟单向悬挂时，用 RelativeContainer 复刻，不用 Column 整组居中

ID：`lesson-e607a28fcd91acd2b40f` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时

## 适用情境

源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。

## 例外与边界

- 兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条

## 原因

只有相邻视图互相双向约束才构成 chain；单向悬挂的兄弟不参与居中，被居中的只有锚定 parent 的那个视图。改成 Column 整组居中后，该视图中心会上移 (间距 + 兄弟高度) / 2。来源中规格把这种布局概括成“垂直居中链”：结构段写对了锚点，决策表却选了 Column 居中，项目级映射基线也写成“居中约束链 → Column 居中”，实现照做。

## 做法

1. 规格提取时逐个子视图记下纵向锚点指向 parent 还是兄弟，再判断是否构成 chain；把决策写成“A 在容器内自身居中，B 以 top 锚 A 底部加间距”，写完与同文件的页面结构段对账；项目级映射基线里的笼统映射按同一规则改成按约束区分。
2. ArkUI 用 RelativeContainer：A 设 .alignRules({ middle: { anchor: '__container__', align: HorizontalAlign.Center }, center: { anchor: '__container__', align: VerticalAlign.Center } })；B 设 .alignRules({ middle: { anchor: '__container__', align: HorizontalAlign.Center }, top: { anchor: '<A 的 id>', align: VerticalAlign.Bottom } }).margin({ top: <源间距> })；被锚定的子组件要设 id。
3. 实现阶段若规格给的是 Column 整组居中，先用源 XML 的 constraint 属性核对；与源约束冲突时按源约束实现，并在转换报告标出。

## 可选检查

- 对居中结果有疑问时，用布局 dump 比较被居中视图的中心与容器内容区中心，单视图居中时两者应重合；无需另起截图任务。

## 来源（按需复核）

- case-6448a485599bfc0740c6 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ee79f91fda0232a915c1fd976889b9b074c5a5ebef6177e7b7704b4c30211b79`
