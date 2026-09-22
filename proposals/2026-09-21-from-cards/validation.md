# 校验结果

以下是独立实验原始阅读包的校验记录。入仓时保留 store revision 与全部 lesson 内容，仅通过发布器重新 `export --link-cards`，生成可在本仓库点击的来源链接；新 manifest 记录对应的文件哈希。原始实验的 `input-cards/` 未重复入仓，相同卡片保存在 `store/cases/`。

运行设置：GPT-5.6 Sol high，零上下文，从 15 张原卡和空库开始，没有提供旧 lesson。使用的归并指令见 [migloop 7690e94](https://github.com/hxy450/migloop/blob/7690e94/skills/migloop-memory-maintain/SKILL.md)，SKILL.md SHA-256 为 `67ae1093f6da5cdd908b6ab2a51f21452749ba5353b48219fed833ef2158678e`。

入仓阅读包另核对 32 个 manifest 文件摘要与 77 个相对链接，全部通过；来源卡与原仓库无差异。上述机械检查不证明每条技术判断或跨项目泛化效果。

结论：通过。

- HEAD revision：`3c8d212f557f1ef86369c96f5eed1d4074909db9722671cf5489f3e10e529a41`，sequence `2`。
- 库内容：15 张可用卡片，12 条经验，19 个主题；经验状态为 `active: 12`，无 `candidate`、`disputed`、`needs_review` 或 `retired`。
- 来源绑定：检查 43 个 `case + claim + revision` 引用，全部可解析且 revision 匹配；去重后覆盖 15/15 张输入卡。
- 阅读包：`memory/manifest.json` 与 HEAD revision 一致；校验 32 个生成文件的 SHA-256，全部匹配 manifest。
- 输入保全：15 个 `input-cards/` 文件的 ID 与 revision 路径有效；其在 `store/cases/` 中的入库副本逐字节一致。维护流程没有向 `input-cards/` 写入。
- 迁移性：在 `memory/` 中检索来源项目名、页面/组件文件名、任务号和历史修复变量，命中数为 0。
- 范围：输出根目录只新增 `store/`、`memory/`、`proposal.yaml`、`merge-notes.md` 和本文件；没有改动其他目录。

阅读入口：`memory/index.md`
