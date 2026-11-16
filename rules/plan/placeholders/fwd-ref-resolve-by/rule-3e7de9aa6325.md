# 登记 FWD-REF 前先读承接切片计划，simple/stub、没有 wires 的切片不能当承接者

审的是：计划与派工
触发（任一种）：
- 读到：覆盖矩阵里承接这个 feature 的切片标为 simple/stub；写错的样子：占位登记里 `FWD-REF` 的 resolve_by 指向一个切片，而那个切片计划里没有 integration_points / wires，也没有对应 Step 写这条接线
适用范围：把页面里的行为登记成前向占位、指定承接切片时
做法：
- 登记前读承接切片的计划，确认 integration_points / wires 或对应 Step 里写了这条接线，才写 resolve_by；没有就不登记，留在本页实现
来源：1 张卡，1 个应用
- case-0ac442a09e1e8ee36a8a（DeepAI全能PPT）：做法第 1 步 ← 建议 1
