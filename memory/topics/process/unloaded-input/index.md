# process/unloaded-input

必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

[上一级](../index.md)

## 本级经验

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](lesson-6a3a7f46c8fec282affa.lesson.md) · 阶段：spec/execute/repair · 信号：Get-Content, Select-String, -Encoding UTF8, $OutputEncoding
- [上下文压缩后按 spec_ref 与源码锚点重读再写计划代码](lesson-f616adca9430826b1661.lesson.md) · 阶段：plan/execute/repair · 信号：spec_ref, feature-index, integration_points, Activity
- [必读 skill 与源码逐份读全，截断即重读再写码](lesson-42df1ac4d4030421da34.lesson.md) · 阶段：spec/execute · 信号：SKILL.md, sed -n, loaded_skills, rg
- [按他文件返回语义改调用方前重读其当前版本](lesson-35f4f9b3cf566d33e79c.lesson.md) · 阶段：execute/repair · 信号：ViewModel
- [编排者代写切片前加载 worker 的全部派工输入](lesson-b90d7f55409a3a34253d.lesson.md) · 阶段：plan/execute · 信号：spec_refs, feature-plan, ui-manifest, Adapter
