# process/input-loading

写前输入是否真的进入上下文：必读 skill、参考与源码片段的读取方式

[上一级](../index.md)

## 本级经验

- [派工指定的必读 skill 及其要求先读的参考要读全再写码：批量读取被截断、只读前 N 行或跳过参考时，规则并未进入上下文](lesson-42df1ac4d4030421da34.lesson.md)
  - 时机：写码 worker 开工时加载派工前置 skill 与参考文档，长会话压缩上下文后继续写码时，以及在回报中填写 loaded_skills 时
  - 情境：派工列出多份前置 skill（常见十几份 SKILL.md），worker 用一次命令批量 cat，或用 sed -n '1,Np' 按固定行数读取；工具对单次输出有长度上限，超出时会省略中段并给出 truncated 提示。也包括已加载的 skill 要求先读某份参考（如迁移陷阱表），worker 没有读，或只在 grep 回执里碰到片段、之后上下文被压缩。
