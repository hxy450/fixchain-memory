# 数据模型里的多值枚举列

agent 会看到什么：读到 feature 规格的枚举表写了三值枚举（如 Auto(0)/Always(1)/Never(2)）、回执备注把几列写成「Int（ordinal/0-1）」；基座规格或数据模型说明把该列写成「Int=0/1」，或把两列的 ordinal 与 0/1 对调

## 规矩

- rule-d99641ddfcb8｜多值枚举列在规格的数据模型里写成 ordinal 枚举并引用枚举表，不写 0/1｜读到：feature 规格的枚举表写了三值枚举（如 Auto(0)/Always(1)/Never(2)），回执备注把几列写成「Int（ordinal/0-1）」；写错：基座规格或数据模型说明把该列写成「Int=0/1」，或把两列的 ordinal 与 0/1 对调
