# ui/text/ellipsis

maxLines + Ellipsis 末行省略粒度

[上一级](../index.md)

## 本级经验

- [maxLines + textOverflow(Ellipsis) 不是 Compose TextOverflow.Ellipsis 的等价物：末行省略粒度不同](lesson-0ebabb99ddeda1f74800.lesson.md)
  - 时机：规格提取阶段，为源码中带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize）的多行正文填写 ArkUI 转换决策及理由时
  - 情境：Android/Compose 多行正文以 maxLines + Ellipsis 折叠；目标 ArkUI Text 用 .maxLines() + .textOverflow({ overflow: Ellipsis })，默认 wordBreak 为 BREAK_WORD；项目口径为完整复刻 Android 可观察行为（D0），视觉核验把平台差异默认计为迁移 bug。
  - 例外：项目允许平台差异（非 D0 完整复刻口径）
