# 身份落地写 app.json5 前，逐项比对验收门禁的模板值规则，冲突在交回前指出

审的是：资源
触发（任一种）：
- 读到：派工或技能要求以受限范围（如 scope=dev-identity）只改部分身份字段，跳过 vendor、bundleName；写错的样子：交回的 app.json5 里 vendor 为 "example"、bundleName 匹配 com.example.*，或 versionName 仍为 "1.0.0"，交回报告里没提这些正是验收门禁的 FAIL / WARN 项
适用范围：应用身份落地阶段，下游有验收门禁检查脚手架默认值时
做法：
- 输出前把 app.json5 现值与验收门禁规则逐项比对：vendor 为 example 即 FAIL，bundleName 匹配 com.example.* 即 FAIL，versionName 为 1.0.0 为 WARN
- 受限范围要求跳过的字段正是 FAIL 项时，在交回报告里写明冲突，不静默保留脚手架值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bundleName 至少三段、点号分隔，推荐反域名形式，如 com.example.demo（第二级为厂商 / 个人名）：com.example.* 是文档示例形式，不是真实厂商（出处：app-configuration-file.md，配置文件标签 bundleName）
针对本应用要查的：
- 下游验收门禁对身份字段的具体规则：流水线验证阶段的检查说明里应用身份那一项；逐条列出 FAIL / WARN 条件，与 app.json5 现值对照
来源：1 张卡，1 个应用
- case-15465539e78d3d899b47（CleanSweep）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
