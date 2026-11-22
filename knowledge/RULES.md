# 配知识的规则

**新写的知识照 `skill/` 做**：流程在 `skill/SKILL.md`，规则在 `skill/references/rules.md`（去哪查、出处、版本在 `skill/references/sources.md`，文件格式在 `skill/references/knowledge-format.md`），给写的人、专门复核的人、抽查的人的任务书在 `skill/briefs/`。新写的文件是新格式（顶层 `id`；`sdk` 另记 `verified_on`、`docs_commit`、`docs_date`；条目没有 `scope`，条数不设上限），检查和渲染用本目录的 `check.py`、`render.py`（写知识的人另用 `skill/scripts/` 里带本机出处核对的那一套）。

**第七版规则**（顶层 `lesson`、条目带 `scope`、每条经验最多 6 条）的原文挪到了 `RULES-v7.md` 留档：`lessons/` 里还有按它写的文件，读和维护那些文件时看它；不再按它写新的。

更早的第三版规则的文件（顶层 `id`、`sdk` 只有 `harmony`、`android`）没有单独的规则文档，格式见 `README.md`「格式」一节。
