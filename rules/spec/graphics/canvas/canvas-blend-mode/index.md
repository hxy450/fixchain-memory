# 依赖画布已有内容的混合模式（blendMode）

agent 会看到什么：读到 Compose drawWithContent 里 drawRect(…, blendMode = BlendMode.Plus / Darken) 在同一画布上着色，或 SDK 文档对 blendMode 的混合基底说得不清；规格把它写成兄弟节点的 .blendMode(…, BlendApplyType.OFFSCREEN) 并定为 HARD

## 规矩

- rule-93f15bed550c｜Compose 同画布 drawRect(blendMode) 着色，规格映射成离屏组内 SRC_IN，不写兄弟节点混合｜读到：Compose 源码 Modifier.drawWithContent { drawContent(); drawRect(Brush.linearGradient(…), blendMode = BlendMode.Plus / BlendMode.Darken) } 在同一画布上给已画好的图标、底盘着色；源码注释提示用「layer + srcIn」；写错：规格把渐变层写成图标的独立兄弟节点 Column().blendMode(PLUS / DARKEN, BlendApplyType.OFFSCREEN) 并定为 HARD，把 SRC_IN 蒙版法只列为回退；或映射决策没引用源码里的实现提示
- rule-86ec2efd1adf｜SDK 文档没说清混合基底范围时，规格把依赖画布状态的混合映射标为待真机核验，不定 HARD｜读到：SDK 文档对 blendMode 只说「与其下方画布已有内容混合（possibly offscreen canvas）」，skill 参考里搜不到 blendMode 指引；写错：规格把依赖画布状态的混合映射定为 HARD 统一决策，回退条件写「真机偏色则退回」，而本流程不编译、不上机，回退永远触发不了
