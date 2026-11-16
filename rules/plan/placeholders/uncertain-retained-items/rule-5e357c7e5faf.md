# 上游登记为需实测的不确定项没实测时，保持 retained 并写明待测字段和预期值

审的是：计划与派工
触发（任一种）：
- 读到：上游 TODO 或派工里有 `UNC` 编号的不确定项（如 `P-S1-UNC-…`），写着「注册字体后按实测校正」「若实测不可行则 retained 附因」；写错的样子：回执把该项列进 `uncertain_regions_resolved`、`retained: []`，产物里却没有任何实测记录；代码注释或源码笔记写「数值同值」「≡ 源式」
适用范围：实现阶段处理上游登记的、要求实测校正的映射不确定项时
做法：
- 没做实测的，该项留在 `retained`，附因写明待测的字段（如 fontBoundingBox*、emHeight*、actualBoundingBox*）和预期值（字体 hhea ascender/descender 与 unitsPerEm 之比）
- 「实现可行」不等于「已验证」：注释和笔记里写「近似、待实测」，不写「数值同值」「≡ 源式」
来源：1 张卡，1 个应用
- case-5e1beaa11de7eb15fa6e（2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
