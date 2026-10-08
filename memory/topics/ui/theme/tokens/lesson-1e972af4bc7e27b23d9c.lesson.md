# 追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追加不覆盖

ID：`lesson-1e972af4bc7e27b23d9c` · 版本：4 · 阶段：execute · 主题：[ui/theme/tokens](index.md)

概要：追加主题色时同步写 dark 目录同名键，已有文件只追加

信号：`color.json`, `resources/dark`, `resources/base`, `darkColors`, `lightColors`

## 何时使用

页面转换或资源阶段，为主题色追加颜色资源键时

## 适用情境

源主题有 Light/Dark 两套调色板；目标颜色资源分 base 与 dark 限定目录，多个任务会分别追加，部分文件由模板预置。

## 原因

只追加 base 键时深色下回落到浅色值；用整体写入覆盖已存在的资源文件，会删掉他人或模板写入的键（如启动窗背景色）。把深色值推给“后续任务”而无人承接时，这些键一直没有深色值。

## 做法

1. 为主题色追加 base 键时，同一次按源深色调色板写 dark 同名键。
2. 写前列出目标目录，文件已存在就先读再只追加，不用整体写入覆盖。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [推进阶段前核对约定产物与放行门，待接事项落负责方](../../../process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md)（共享 1 张卡）
- [深浅主题状态放可观察对象，入口同步，组件渲染期读取](lesson-7b19b801e0f21481d1d6.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-2c6857febfce92e5d5bc](../../../../../store/cases/case-2c6857febfce92e5d5bc/0de684fa8dfa58b7980ea4112552df78f4b747c3424b41d244d8715c38816ace.json) · 结论：diagnosis, rec-89b7babdb3
  卡片版本：`0de684fa8dfa58b7980ea4112552df78f4b747c3424b41d244d8715c38816ace`
