# 实体模型字段按源类型真值定型：Double 字段不因 String 入口改存字符串，显式传 null 的字段保留 null，规格缺省值在构造时赋值

ID：`lesson-5a67ac0592e5a3fa20b9` · 版本：3 · 阶段：spec/execute · 主题：[data/model](index.md)

概要：实体字段按源类型真值定型，null 与空串分开

信号：`Parcel`, `String.valueOf`, `cursor.getString`, `ResultSet.getString`, `getDouble`, `getColumnType`, `CursorWindow`, `parseDouble`, `Double.toString`, `%g`

## 何时使用

规格提取与模型、数据库层实现阶段，把 Java 实体（含继承外部库基类的实体）的字段类型、缺省值与可空性写成目标模型、落库绑定与读回逻辑时

## 适用情境

源实体字段声明为 Double/Long 等装箱数值，却另有 setXxx(String) 重载、Parcel 以 String.valueOf 写出、页面以 "" 调 setter；某条构造路径显式给引用字段传 null；规格表给出无参构造的缺省值（如当前毫秒作 id）；DAO 以 cursor.getString 读回 REAL 列。目标准备用 string | null 存数值、以 '' 兼表 null、把缺省值推给仓储层、把 getString 一对一换成 ResultSet.getString。

## 原因

存储类型取自 String 入口时，空串会以 TEXT '' 落库而不是 NULL，读回与序列化的类型也随之偏离；'' 兼表 null 后，落库值与 JSON 是否省略键无法再按原值判定；缺省值改由仓储补，构造后、落库前读到的对象就与源端不同。Android CursorWindow 对 REAL 列的 getString 按 "%g"（6 位有效数字）成文（AOSP android_database_CursorWindow.cpp nativeGetString），relationalStore 的 getString 对 DOUBLE 列的文本形态与 "%g" 不同，且官方注明可能丢精度、建议用 getDouble（HarmonyOS 文档 arkts-apis-data-relationalstore-resultset，访问于 2026-10-17），一对一替换会改变读回值。

## 做法

1. 字段类型以类型真值为准（实体声明、参考设计或基类字节码给出的 Double/Long）；String 入口另写成访问器契约，如 setXxx(String) = parseDouble、解析失败为 null，数值转文本按 Double.toString 规则。
2. 按源构造器与调用点区分 null 与 ""：任一路径显式传 null 的引用字段，目标保留 T | null；落库写 NULL、JSON 省略键都按原值判定。
3. 规格表或源无参构造给出的缺省值在目标构造时赋值；要改由仓储补值，先回源码确认无参构造确实不赋值并注明出处。
4. Double 字段落库按数值绑定（空串或不可解析为 NULL）；源端以 cursor.getString 读 REAL/INTEGER 列再解析时，按 getColumnType 分列类型复刻源平台文本形态（REAL 列先 getDouble 取值，再按 C "%g" 成文）后再按源端解析。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [结论先查本机 SDK 与依赖源，查不到才标置信度](../../process/unverified-as-fact/lesson-c0f990ea57a901951ba8.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-5e7f81b1b1ef0753d249](../../../../store/cases/case-5e7f81b1b1ef0753d249/203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b.json) · 结论：diagnosis, rec-f612e33d8c, rec-5467d118e9, rec-d6770e9a04, rec-f8e24269d1
  卡片版本：`203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b`
