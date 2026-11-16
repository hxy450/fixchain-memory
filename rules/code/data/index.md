# 数据与存储

源端有 SharedPreferences / MMKV、Room / SQLite、Gson / org.json 模型、XML 解析、Repository / Dao 的调用和同步进度事件、文件读写和 ZIP、种子数据，目标端有 preferences、relationalStore、模型 class、JSON.parse、fs 读写时

## 子主题

- [数据库](database/index.md)（19 条）：源端有 Room 的 @Database / @Entity / @PrimaryKey / Migration、SQLiteOpenHelper，目标端有 relationalStore 的 getRdbStore、CREATE TABLE、insert、事务时
- [数据模型与解析](model/index.md)（39 条）：源端有 Kotlin data class / Java bean、Gson 的 @SerializedName、org.json 的 JSONObject、enum、SAX / XmlPullParser，目标端有模型 class、JSON.parse 后的取值、@ohos.xml 解析时
- [偏好存储](preferences/index.md)（17 条）：源端有 SharedPreferences、MMKV 的读写，目标端有 preferences 的封装、putSync / flush 和它用的 Context 时

## 触发族

- [照源码移植的 Service、Repository 和 Dao 调用](repository-port/index.md)（4 条）：读到源端 Service / ViewModel 经 Repository、Dao 的调用（分阶段的缓存读写、@Body 请求体的组装、按多个键的查询）；产物里移植后的方法少了调用、参数或字段：漏掉某阶段的副作用、写方法没有调用者、body 写成 {}、少了月份键
- [同步和后台操作的进度、状态事件](sync-status-events/index.md)（4 条）：读到源端同步序列发进度事件（开始 0、结束 100、失败）的门控和时机、保存之后的收尾步骤；产物里进度事件发的时机或次数不对、catch 写进了别的操作的状态字段、保存后少了当前项的校验和写回
- [共享和按成员两种完成状态的 userId 写入](shared-member-userid/index.md)（2 条）：读到源端完成状态分共享（任一成员完成即完成、不写 userId）和按成员两种、重复事件另按日期区分；产物里的写入键 userId、撤销和子项删除的 where 条件，以及对应的测试用例
- [文件读写、建目录和 ZIP 打包](file-io-zip/index.md)（11 条）：读到源端用 File.mkdirs / createOrExistsDir、FileInputStream、listFiles、ZipOutputStream.putNextEntry 和 catch (OutOfMemoryError) 读写文件、打包导出；产物里 fs / fileIo 的 mkdirSync、statSync、手写 ZIP 或 zlib 的对应写法
- [演示和种子数据](seed-data/index.md)（1 条）：读到计划或 feature-index 写明演示数据依赖源端的种子类、模板类，并给出 spec_ref 指向的功能 spec；产物里写演示行的代码，标题、日期偏移、主题 key、清单项和完成状态是自拟的，主题 key 换成了 #RRGGBB 颜色串
- [DAO 读写里的加解密钩子](dao-crypto-hook/index.md)（2 条）：读到安卓 DAO 的读写方法里无条件 encrypt(...) / decrypt(...)，或备份导出导入对 DAO 记录再加解密；产物里 DAO 的加解密钩子 setter（默认恒等或空实现）注入在业务单例 getInstance() 里还是 EntryAbility.onCreate，导出导入任务开始前有没有确保钩子已注入
