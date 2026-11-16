# 没有真机 dump、由源码合成的基线快照

agent 会看到什么：基线快照的 meta.json 标 view_xml_synthesized 或 confidence medium、bounds 为空、没有真机 UIAutomator dump，规格把源码字面 dp 直接写成「判:visual」判据，或写「近乎不可见」「parity 保留」这类定论

## 规矩

- rule-4be237c4364a｜ui-snapshot 是合成的时，带具体 dp 的视觉验收条目标 confidence=medium｜读到：没有真机 UIAutomator dump，ui-snapshot 由源码合成、bounds 为空（meta 标 confidence medium）；写错：功能规格里「判:visual」的验收条目直接把源码字面 dp 写成判据（如「36×36 圆形、距状态栏 10vp、距左 16vp」），没带 confidence=medium
- rule-67342d8a277d｜快照自述无真机 dump 时，「近乎不可见、parity 保留」类结论降级为待真机核对项｜读到：基线快照 meta.json 标注 `view_xml_synthesized`、bounds 为空、无真机 UIAutomator dump；写错：规格或决策台账写「浅色近乎不可见」「parity 保留」「忠实复刻」，把它当已知缺陷要求实现者原样画出
