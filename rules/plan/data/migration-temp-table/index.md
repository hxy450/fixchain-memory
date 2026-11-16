# 数据库迁移里建了又改名的 *_new 表

agent 会看到什么：源端 Migration.migrate 里 CREATE TABLE x_new、拷数据、DROP 旧表后 RENAME 回原名，对照或修复工作清单把 x_new 列成目标缺的表

## 规矩

- rule-121ba627ee8a｜只在 Migration.migrate 里建、随后 RENAME 的 *_new 表按迁移临时表处理，不列为缺表｜读到：源端某个 Migration.migrate 里 CREATE TABLE x_new、拷数据、DROP TABLE x 后 ALTER TABLE x_new RENAME TO x；写错：对照或修复工作清单把 x_new 列为目标缺的表，要求为它建持久模型
