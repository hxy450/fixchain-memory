# 排除决定落到计划时保留可逆性：单列 deferred 批次，不批量打墓碑删映射

审的是：计划与派工
触发（任一种）：
- 读到：决策台账把某个功能簇（如桌面 Widget）按政策排除；写错的样子：计划把该功能的 parity AC 全部批量打上「superseded by」决策编号的墓碑，并从 plan-coverage 的批次映射里删掉
适用范围：规划阶段落地按政策排除的功能簇时，计划、覆盖清单和跳过清单
做法：
- AC 原样保留，给这簇功能单列一个批次标 deferred，plan-coverage 里保留它的映射
来源：1 张卡，1 个应用
- case-dc1f3f5507c9cd8ad208（omni-notes-hmos）：做法第 1 步 ← 建议 3
