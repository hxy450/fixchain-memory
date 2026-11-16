# 带 String 重载或 Parcel 字符串写法的数值字段

agent 会看到什么：读到参考文档或 getter 给出模型字段是 `Double` / `Long`，同时有 `setX(String)` 重载，或 Parcel 里写 `String.valueOf(getX())`、读 `setX(in.readString())`；规格字段表把存储类型写成 string、建议目标用 `string | null` 存，或没写 String 入口的解析规则

## 规矩

- rule-57fb7b54c298｜源字段已有 Double/Long 真值时，规格不因 String 重载或 Parcel 写法改成 string｜读到：参考文档或 getter 给出字段是 `Double` / `Long`，同时有 `setX(String)` 重载，或 Parcel 里写 `String.valueOf(getX())`、读 `setX(in.readString())`；写错：规格字段表把存储类型写成 string，或写「setter 同时接受 String 与数值」并建议目标用 `string | null` 存储；String 入口的解析规则没有写
