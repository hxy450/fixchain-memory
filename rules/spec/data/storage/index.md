# 数据库、JSON 与文件

读到 SQLiteOpenHelper、Room @Entity、org.json、assets/ 下的预置 JSON 或 DB、种子数据类、外部存储公共目录和 MediaStore，规格里写数据表、逐列清单、建库时机、解析和下载导出时

## 触发族

- [源工程 assets/ 下的预置数据](preset-assets-data/index.md)（2 条）：源工程 assets/ 下有按日期等键查表的预置 JSON 或 DB，规格引用它却没写覆盖范围、没和运行期输入比对，或数据流写成「资产 + DAO」而源码实际层层委托到第三方库计算
- [源码用 org.json 读写 JSON](org-json/index.md)（4 条）：源码 import org.json，用 new JSONObject(...)、getString / getInt / getJSONObject / getJSONArray、put、toString 解析或导出，或在循环里边解析边 insert，规格写成 JSON.parse 纯语言构造、「null 键保留」或「解析先于写库」
- [SQLiteOpenHelper 子类的建库时机](sqlite-open-helper/index.md)（1 条）：读到数据库 helper extends SQLiteOpenHelper、构造只调 super(...)、没人调 getReadableDatabase / getWritableDatabase；规格写「构造即建库」「空库照建」
- [源工程种子类构造的固定演示数据](seed-demo-data/index.md)（1 条）：读到源工程用种子类、模板类构造固定演示数据（固定标题、日期偏移、主题 key、完成集合）；规格只概括记录数和完成比例，主题写成颜色的中文译名，没逐项列出数据表
- [源端读写外部存储公共目录和 MediaStore 媒体库](public-storage-media/index.md)（5 条）：读到源码申请 WRITE_EXTERNAL_STORAGE / READ_MEDIA_AUDIO，下载到公共目录后发 ACTION_MEDIA_SCANNER_SCAN_FILE，或查询 MediaStore.Audio 列本地音频；规格的下载链没有导出步骤、把媒体扫描标「不迁移」，或写成 MediaLibraryKit 查询加权限申请
- [Room 实体的列清单](room-columns/index.md)（1 条）：源端 Room 的 @Entity / @ColumnInfo 和导出 schema 里的 createSql；源码笔记或 brief 里给出的逐列清单
- [数据模型里的多值枚举列](enum-ordinal-column/index.md)（1 条）：读到 feature 规格的枚举表写了三值枚举（如 Auto(0)/Always(1)/Never(2)）、回执备注把几列写成「Int（ordinal/0-1）」；基座规格或数据模型说明把该列写成「Int=0/1」，或把两列的 ordinal 与 0/1 对调
- [Room 数据库的文件名（databaseBuilder 的 name）](room-database-name/index.md)（1 条）：读到源端 Room.databaseBuilder(context, klass, name) 的 name 参数没有 .db 后缀；规格写「Room `<名>.db`」或「备份 zip 内含 <名>.db」，备份互导的归档条目名凭印象补了 .db
