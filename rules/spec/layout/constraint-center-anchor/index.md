# ConstraintLayout 里四向锚 parent 的单视图和挂在它下面的兄弟

agent 会看到什么：读到源布局 ConstraintLayout 里一个子视图 start/end/top/bottom 都锚定 parent，兄弟视图只有 constraintTop_toBottomOf 指向它、兄弟之间没有反向约束；规格把根布局写成「N 个子元素的垂直居中链」「ConstraintLayout（居中约束链）→ Column」

## 规矩

- rule-7013218629f9｜单视图四向锚 parent、兄弟只挂其下时，规格写单视图居中，容器选 RelativeContainer｜读到：源布局 ConstraintLayout：一个子视图 start/end/top/bottom 四向锚定 parent，兄弟视图只有 constraintTop_toBottomOf 指向它，兄弟之间没有反向约束；写错：规格把根布局概括成“N 个子元素的垂直居中链”，转换决策写 Column 整组居中、理由“无相对约束需求”；或跨栈映射基线写“ConstraintLayout（居中约束链）→ Column”
