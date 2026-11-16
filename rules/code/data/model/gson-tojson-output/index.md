# Gson 反射序列化写出的 JSON

agent 会看到什么：读到源端备份或互通 JSON 走 new Gson().toJson(obj) / GsonBuilder 反射序列化，参考里的 JSON 示例标着 [推断]；产物里手写 toJson 的键序、Boolean 写法、null 键是否写出，或 JSON.stringify 加全局 replace 凑 htmlSafe 转义

## 规矩

- rule-b6e6e4cb12cc｜源端用 Gson 反射写备份 JSON 时，toJson 按 Gson 的键序、布尔写法和 null 省略写出｜读到：源端备份或互通 JSON 走 `Gson` 反射序列化（`new Gson().toJson(obj)`），规格或参考里的 JSON 示例标着 `[推断]`；写错：手写的 `toJson` 照抄推断示例：Boolean 字段写成 0/1 数值、null 值写出键、键序不按字段声明顺序，或用 `JSON.stringify` 加全局 `replace` 凑 htmlSafe 转义
