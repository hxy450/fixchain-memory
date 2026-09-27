# ui/layout

容器选择、约束与定位（ConstraintLayout、RelativeContainer、Column 等）

[上一级](../index.md)

## 本级经验

- [ConstraintLayout 中单视图对 parent 居中、兄弟单向悬挂时，用 RelativeContainer 复刻，不用 Column 整组居中](lesson-e607a28fcd91acd2b40f.lesson.md)
  - 时机：规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时
  - 情境：源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。
  - 例外：兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条
