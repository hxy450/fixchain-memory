# 备份归档的条目名常量照源端 Room 库文件名写，不带 .db

审的是：代码
触发（任一种）：
- 读到：源端 Room.databaseBuilder(context, klass, name) 的 name 没有 .db；写错的样子：目标端备份代码里 zip 条目名常量写成带 .db 的名字（注释引规格的工件契约），压缩时按这个名归档
适用范围：目标端自实现与源端互导的备份 zip 时
做法：
- zip 条目名常量写成源端 databaseBuilder 的 name 原样（返修把条目改成不带 .db 的库名）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 数据库文件名就是传入的 name：getDatabasePath(name) 在数据库目录下 new File(base, name)，不加后缀：源端库文件和归档条目都不带 .db（出处：android.app.ContextImpl#getDatabasePath、android.app.ContextImpl#makeFilename）
针对本应用要查的：
- 源端数据库文件名：源工程里 Room.databaseBuilder(...) 调用的第三个参数；照字面写成条目名常量
来源：1 张卡，1 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 建议 3、诊断
