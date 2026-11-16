# SQLiteOpenHelper 子类的建库时机

agent 会看到什么：读到数据库 helper extends SQLiteOpenHelper、构造只调 super(...)、没人调 getReadableDatabase / getWritableDatabase；规格写「构造即建库」「空库照建」

## 规矩

- rule-bafdddcb627d｜源端只 new 一个 SQLiteOpenHelper 子类时，规格写构造不建库、首次 get*Database 才建｜读到：数据库 helper extends SQLiteOpenHelper，构造只调 super(...)，之后没人调 getReadableDatabase / getWritableDatabase；写错：规格写「空库照建（构造即建库）」「空库导出空 content」，备份契约假定库文件总存在
