# process/sdk-reading

核 SDK d.ts 的方法

[上一级](../index.md)

## 本级经验

- [核 SDK d.ts 时读字段的 doc 行与语义段，不只 grep 签名](lesson-5ebfd81b0d3ff8f55999.lesson.md)
  - 时机：规格提取或界面实现阶段，用 grep/sed 在 SDK d.ts 里核对某个 ArkUI 属性、接口字段或方法是否可用、单位/语义是什么时
  - 情境：grep 命令只保留签名行（`radius: number | Resource;`、`lineHeight(value: …)`、`blendMode(…)`、`BorderOptions`），紧邻的 `/** … unit is px */` 或语义描述被过滤掉；随后据此写契约或定 HARD。
