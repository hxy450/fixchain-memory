# 只在 Migration.migrate 里建、随后 RENAME 的 *_new 表按迁移临时表处理，不列为缺表

审的是：计划与派工
触发（任一种）：
- 读到：源端某个 Migration.migrate 里 CREATE TABLE x_new、拷数据、DROP TABLE x 后 ALTER TABLE x_new RENAME TO x；写错的样子：对照或修复工作清单把 x_new 列为目标缺的表，要求为它建持久模型
适用范围：数据层对照、判官分诊和修复派工里核对缺表时
做法：
- 缺表对照以最终 schema 的实体为准，迁移临时表不算；清单里应修的写成补库版本和升级路径
来源：1 张卡，1 个应用
- case-a3f7f5fbc8635b723b96（Cofi）：做法第 1 步 ← 建议 4、诊断
