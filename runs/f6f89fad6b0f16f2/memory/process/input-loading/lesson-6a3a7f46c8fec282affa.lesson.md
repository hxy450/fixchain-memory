# Windows PowerShell 5.1 读取 UTF-8 中文规格与账本要显式 -Encoding UTF8；回执出现乱码就当作没读

ID：`lesson-6a3a7f46c8fec282affa` · 版本：1

[本主题](index.md)

## 何时使用

规格提取、切片实现与接线阶段，在 Windows PowerShell 5.1 下用 Get-Content/Select-String 读取功能规格、决策账本或中文注释源码时

## 适用情境

迁移工程的规格、决策账本与计划为 UTF-8（无 BOM）中文 Markdown；读取者在 Windows PowerShell 5.1 中不带编码参数读取，回执里中文段落变成成片乱码，AC 编号、方法名、路径等 ASCII 片段仍然可读。

## 原因

Windows PowerShell 5.1 的 Get-Content/Select-String 默认按系统 ANSI 代码页解码无 BOM 的 UTF-8 文件，中文条款变成乱码而 ASCII 标识照常显示，读取者容易以为已经读到了条款。来源为同一应用的多次切片实现：实现者读到的功能规格中文正文均为乱码，只凭 AC 编号与方法名实现，漏掉了“成功后才写缓存”“先授权再定位、拒绝不能静默”“登录成功后重载任务数据”等只写在中文正文里的条件。

## 做法

1. 在 PowerShell 5.1 中读取文本一律带编码：Get-Content -Raw -Encoding UTF8、Select-String -Encoding UTF8；批量读取前也可先设置 $OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()。
2. 回执里出现成片乱码时，把该文件视为未读，用 UTF-8 重读后再据此实现；不要凭可读的 AC 编号、方法名推断条款内容。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-46ac36102451125de693 · 结论：diagnosis, recommendation:3
  卡片版本：`a6c8db979bd0752f20fae73d52994a8dbee33b35ca5a2e883679aeca400ed09a`
- case-8c249997059a2524ea7b · 结论：recommendation:3
  卡片版本：`b68039d3741ec70ee43c59d40fbd4d1570b96692f9d2f6c03c39704123cc1427`
- case-fa7bbda457517260efc4 · 结论：diagnosis, recommendation:5
  卡片版本：`13060717bdfc19afb975d9cd93d6c841d9e637fde59c3eb5f8e6b8ab8e892577`
