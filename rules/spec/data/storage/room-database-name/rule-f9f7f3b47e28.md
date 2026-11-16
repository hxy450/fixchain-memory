# 声明与源端备份互导时，规格里的归档条目名取 Room databaseBuilder 的 name，不自动加 .db

审的是：规格
触发（任一种）：
- 读到：源端 Room.databaseBuilder(context, klass, name) 的 name 参数没有 .db 后缀；写错的样子：规格写「Room `<名>.db`」或「备份 zip 内含 <名>.db」，条目名凭印象补了 .db，没对照 databaseBuilder 的声明
适用范围：规格声明目标端备份与源端备份双向兼容时的归档条目名
做法：
- 归档条目名取源端实际文件名：Room databaseBuilder 的 name 参数就是库文件名，不加 .db；有条件时用源端导出的样本包核对条目列表
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 数据库文件名就是传入的 name：getDatabasePath(name) 在数据库目录下 new File(base, name)，不加后缀：name 没写 .db，磁盘上的库文件就没有 .db（出处：android.app.ContextImpl#getDatabasePath、android.app.ContextImpl#makeFilename）
- 导出条目是 Room 库文件名本身；条目若叫 <名>.db，安卓端导入后 Room 打开的是新建的空库：反编译 AAR 确认的行为（出处：卡里修好并验证过）
针对本应用要查的：
- 源端数据库文件名：源工程里 Room.databaseBuilder(...) 调用的第三个参数；照字面写成条目名，不加也不去后缀
来源：1 张卡，1 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 建议 3；取值 2 ← 诊断
