# 被记成降级的界面视觉效果（自绘组件、输入框富文本）

agent 会看到什么：读到源端界面有自绘视觉组件（如 Material3 Expressive 的 CircularWavyProgressIndicator）或输入框 visualTransformation 富文本；skip-list、决策台账或转换决策把它记成「实现降级」「能力受限，编辑态降级」的 PD 或已批降级，没核对 Canvas / Path、RichEditor 等候选组件

## 规矩

- rule-206c80e34304｜目标能用 Canvas/Path 自绘的视觉效果不登记为平台无对等 PD，写成实现项并附源参数｜读到：源端用 Material3 Expressive 这类自绘视觉组件，如按偏好在 CircularWavyProgressIndicator 与 CircularProgressIndicator 之间切换；产出定位写着「完整复刻」；写错：skip-list 或决策台账把它登记为「实现降级」的 `PD-` 条目，平台约束写「可移植但复杂度高 / 成本高 / 首版无必要 / 暂不」，并列进「直接砍掉范围」
- rule-82d5ad3b95a2｜规格写「目标能力受限需降级」前先核对候选组件，未核实的不写成已批降级｜读到：源端输入框带 `visualTransformation`（如按 URL 构造带样式的 AnnotatedString）等富文本效果；写错：规格转换决策表写「ArkTS 输入框内富文本高亮能力受限，编辑态降级、保底纯文本」，没有核对 RichEditor 等候选组件；后续 uncertain 复审直接沿用
- rule-460f46c437f3｜规格判定「编辑态无可点击 span」前先查 RichEditor 声明，替代通道标为行为差异｜读到：安卓源用三方 EditText 在编辑态给正文内的链接加可点击 span（如 gatherLinksForText + setOnTextLinkClickListener）；写错：规格断言「ArkUI TextInput/TextArea 不支持编辑态内嵌可点击 span」「RichText 只读」，据此登记决策改走替代通道（如长按 → 解析全文 → 动作列表），映射行仍标 HARD 行为等价
- rule-075f852f8893｜规格以「知识库无条目」判 HARD-DIV 时，改为引 SDK d.ts 证据，查不到写「待验证」｜读到：源端用 BetterLinkMovementMethod 按触点找 ClickableSpan 再派发点击或长按；规格模板要求平台能力结论以 SDK d.ts、knowledge-verifier 查证或参考条目为据；写错：规格以「arkts-knowledge-verifier 无 span 级手势条目」为据判 HARD-DIV，替代路径写「命中域=整个文本组件 → URL 提取」，并作废 span 级触摸 AC
