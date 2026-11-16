# Room 数据库的文件名（databaseBuilder 的 name）

agent 会看到什么：读到源端 Room.databaseBuilder(context, klass, name) 的 name 参数没有 .db 后缀；规格写「Room `<名>.db`」或「备份 zip 内含 <名>.db」，备份互导的归档条目名凭印象补了 .db

## 规矩

- rule-f9f7f3b47e28｜声明与源端备份互导时，规格里的归档条目名取 Room databaseBuilder 的 name，不自动加 .db｜读到：源端 Room.databaseBuilder(context, klass, name) 的 name 参数没有 .db 后缀；写错：规格写「Room `<名>.db`」或「备份 zip 内含 <名>.db」，条目名凭印象补了 .db，没对照 databaseBuilder 的声明
