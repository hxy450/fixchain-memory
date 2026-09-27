# data/schema

Room 到 relationalStore 的库名、schema 版本、建表语句与升级路径

[上一级](../index.md)

## 本级经验

- [Room 数据库落成 relationalStore 时保留库名、schema 版本与显式升级路径；迁移代码里的 xxx_new 是临时表](lesson-a6f300f9295ba538f23b.lesson.md)
  - 时机：数据层实现阶段，把 Room 数据库落成 relationalStore，确定库名、schema 版本、建表语句与升级路径时；以及评审或修复分诊缺表问题时
  - 情境：源端 Room @Database 声明 version，配 addMigrations/AutoMigration 与 fallbackToDestructiveMigration，迁移代码用 xxx_new 临时表重建后 RENAME；规格要求显式版本化迁移、保留源 schema 历史与字段可空性。
