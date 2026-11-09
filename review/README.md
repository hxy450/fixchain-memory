# e613047f 修订依据

本分支发布既有完整修订候选：521条活跃Memory，其中137条正文修订、384条未改。

- [逐条修订记录](revisions.json)：原文与修订哈希、具体替换、修订理由、引用原文、证据文件及适用限制。
- [完整Memory入口](../memory/index.md)。
- `evidence/`保存实际引用的证据快照；文件名为SHA-256，`revisions.json`中的路径相对本目录。官方资料、历史案例、源码及其他Memory分别作为对应主张的依据，不能一概当作官方合同。

基线提交：`9fda5ccc79e52d31cec68e0dbd51c3e66b5e4bac`。
来源候选提交：`ab77b27ec2393c4c1d6c6cb84d4639df4d72b4bf`。

候选manifest的父版本字段记录历史文本候选链，不对应本分支重新生成的store快照。

Memory正文与原候选字节一致，官方证据没有额外插入正文。本目录是随分支交付的修订依据；它不包含评测答案、模型凭据或完整外部评测仓库。`store/`保留原始案例，Memory文本候选版本以`memory/manifest.json`为准。
