# process/convergence

收敛/收尾阶段的对账与风险处置

[上一级](../index.md)

## 本级经验

- [收敛 worker 的派工清单逐条列出 mapping 中的全部共享原语，worker 逐项对账后再整文件重写](lesson-61a5ff18acd76d13dad3.lesson.md)
  - 时机：收敛阶段，派发 W2 类 worker 把页面私有实现替换为共享基座原语（阴影/排版/颜色映射函数）并允许其整文件重写时
  - 情境：mapping 文档已有共享原语节（如 §5 shadowFor），页面内联写法与之不一致；派工清单只点名部分对接点。
- [结构收敛不等于行为核验：风险标记的 AC 与 forward-ref 占位不得凭收敛结果清除或写进 impl_claims](lesson-841ee37c9e648274d76c.lesson.md)
  - 时机：收敛/收尾阶段，closer 或主会话把 worker 回执里点名的风险 AC 写进 impl_claims、或解除 forward-ref-uncertain 占位标记时
  - 情境：worker/closer 已把某 AC 标为风险且只能 ui 判定（如 AC67 被 converter、Slice 5、closer 三次标记），或共享件带 forward-ref-uncertain 占位（P-S6-002 iconTintLayer）；生成期禁编译/无真机。
  - 例外：已有截图/dump 或等价单测证据
