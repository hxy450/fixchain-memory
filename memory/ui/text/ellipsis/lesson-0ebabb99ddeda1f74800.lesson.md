# maxLines + textOverflow(Ellipsis) 不是 Compose TextOverflow.Ellipsis 的等价物：末行省略粒度不同

ID：`lesson-0ebabb99ddeda1f74800` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，为源码中带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize）的多行正文填写 ArkUI 转换决策及理由时

## 适用情境

Android/Compose 多行正文以 maxLines + Ellipsis 折叠；目标 ArkUI Text 用 .maxLines() + .textOverflow({ overflow: Ellipsis })，默认 wordBreak 为 BREAK_WORD；项目口径为完整复刻 Android 可观察行为（D0），视觉核验把平台差异默认计为迁移 bug。

## 例外与边界

- 项目允许平台差异（非 D0 完整复刻口径）

## 原因

Compose/StaticLayout 末行按字符贪心填满再接「…」；ArkUI 默认按词换行后末行放不下整词就整词丢弃、再接带前导空格的「 ...」并留白。spec 写前未读任何映射参考就把两者标为「等价」；映射参考本身只记 API 对应（ellipsize → textOverflow），pitfalls 只说省略号须显式设置，都没有粒度差异记录。

## 做法

1. 转换决策不写「等价」：写明 ArkUI 末行按词丢弃再补「 ...」与 Android 按字符填满再接「…」的差异；D0 口径下登记为平台差异项（PD）或直接给出实现方案。
2. 映射参考只给 API 对应时，检查它是否覆盖渲染语义；缺口写进 spec 的差异 AC，而不是留给视觉核验补票。

## 检查

- 双端截图对比折叠段落末行：字符截断位置与省略号前是否有空格。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-b57f1b660260b8843ce3](../../../../store/cases/case-b57f1b660260b8843ce3/6be8a93eda7e3ab3d2d6439f2891be2a742037ef97f4e39b0f675053efcb3a2a.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`6be8a93eda7e3ab3d2d6439f2891be2a742037ef97f4e39b0f675053efcb3a2a`
