# 源端库只在首次打开时创建，目标不在启动 init 里 getRdbStore 预建库

审的是：代码
触发（任一种）：
- 读到：数据库 helper extends SQLiteOpenHelper，构造只调 super(...)，正常路径上没有 getWritableDatabase 调用；写错的样子：目标启动服务或备份服务构造里 fire-and-forget 调 init() → relationalStore.getRdbStore(...) 建库，备份前先 await 这个建库任务
适用范围：源端 SQLiteOpenHelper 数据库迁成 relationalStore、且有备份恢复链路时
做法：
- 启动时不调 getRdbStore 预建库；备份和恢复按源路径：先判断库文件是否存在，不存在时备份按失败处理，存在才打开
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getRdbStore(context: Context, config: StoreConfig): Promise<RdbStore>；沙箱路径下没有库文件时会创建：调用它就会建库，不能用来「只打开已有库」（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，relationalStore.getRdbStore；arkts-apis-data-relationalStore-f.md，relationalStore.getRdbStore）
- 去掉启动建库、增加库文件存在判断和不建库的打开路径后，库文件不存在时备份失败，与源端一致：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ad0ab84cef0e7cbc3696（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
