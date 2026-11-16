# Room 实体的列清单

agent 会看到什么：源端 Room 的 @Entity / @ColumnInfo 和导出 schema 里的 createSql；源码笔记或 brief 里给出的逐列清单

## 规矩

- rule-9931a57551ef｜源码笔记为手写 DDL 列 Room 列清单时，附原始 createSql 或标出关键字列名｜读到：Room 导出 schema 的 <version>.json 里每张表有 createSql；@ColumnInfo(name = …) 的列名含 to、order、group 这类 SQL 关键字；写错：数据层的源码笔记或 brief 只给逐列清单（表、列名、类型、可空），没附 createSql，也没标出属于 SQL 关键字的列名
