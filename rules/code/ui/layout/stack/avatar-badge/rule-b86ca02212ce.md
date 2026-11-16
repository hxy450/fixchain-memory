# 源头像控件没有描边时，目标头像不留 border，重叠头像逐属性对照源 item

审的是：代码
触发（任一种）：
- 读到：源头像 item 是固定尺寸 `<FrameLayout>` 里的 `ImageView`（`android:scaleType="centerCrop"`），没有 stroke 一类描边属性，多个头像按固定步距重叠；写错的样子：目标头像带 `.border({ width: 1, color: … })` 一类白描边（沿用目标旧代码），重叠处显出竖线
适用范围：迁移重叠排列的头像、成员列表 item 时
做法：
- 逐属性对照源 avatar item：容器尺寸、头像尺寸、scaleType、有无 stroke、重叠步距；源端没有描边就删掉 .border
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 删除描边后头像间竖线消失：修法已上机验证（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c9cc6663456a2ef02f89（记得日历）：做法第 1 步 ← 建议 2、诊断；取值 1 ← 诊断
