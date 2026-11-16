# 占位因「库源不可见」登记 forward-ref-uncertain 时，不以视觉对齐为 resolve_by

审的是：计划与派工
触发（任一种）：
- 读到：页面规格写「三方库内部 UI 不可见 → 自研 / 近似」；写错的样子：占位登记里有 `forward-ref-uncertain` 的 `UNC` 条目，原因是「AAR 无源可查 / 库源不可见」，resolve_by 写「Slice N Step 3a 视觉对齐」
适用范围：实现阶段登记占位或移交项，原因是缺三方库的源码或制品时
做法：
- 原因是缺库制品时，不以「视觉对齐」作为 resolve_by（没有真值就无从对齐）；回报缺库制品的阻塞，或自行取 AAR 按真值实现后再登记
来源：1 张卡，1 个应用
- case-74b07cb94daa311f36b1（omni-notes-hmos）：做法第 1 步 ← 建议 3
