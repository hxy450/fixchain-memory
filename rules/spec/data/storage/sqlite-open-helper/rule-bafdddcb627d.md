# 源端只 new 一个 SQLiteOpenHelper 子类时，规格写构造不建库、首次 get*Database 才建

审的是：规格
触发（任一种）：
- 读到：数据库 helper extends SQLiteOpenHelper，构造只调 super(...)，之后没人调 getReadableDatabase / getWritableDatabase；写错的样子：规格写「空库照建（构造即建库）」「空库导出空 content」，备份契约假定库文件总存在
适用范围：规格提取时写数据库创建时机和备份读侧对库文件的假定
做法：
- 规格写明：SQLiteOpenHelper 构造不建库，首个 getReadableDatabase / getWritableDatabase 才建；没有调用方时库文件不存在
- 备份读侧写成「库文件缺失即失败」，目标不在启动时预建库
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SQLiteOpenHelper 构造只创建 helper 对象，直到调用 getWritableDatabase 或 getReadableDatabase 才真正创建或打开数据库：构造不建库（出处：android.database.sqlite.SQLiteOpenHelper#SQLiteOpenHelper）
- 库文件不存在时源端备份失败，目标预建库后备份总成功；去掉启动建库后一致：两端行为差异（出处：卡里修好并验证过）
针对本应用要查的：
- 源端有没有调用方真正打开库：源工程 Java/Kotlin 里该 helper 的 getReadableDatabase / getWritableDatabase 调用点（DAO 等）；正常使用路径上没有调用时，契约写成库文件不存在
来源：1 张卡，1 个应用
- case-ad0ab84cef0e7cbc3696（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 2 ← 诊断
