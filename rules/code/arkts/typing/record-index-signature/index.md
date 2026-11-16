# Record 类型和索引签名

agent 会看到什么：读到或写出 Record<K, V>、[key: string] 索引签名、标识符键的 Record 字面量，构建日志报 arkts-no-indexed-signatures / arkts-no-props-by-index / arkts-no-untyped-obj-literals

## 规矩

- rule-15eda3782bd2｜按规范去掉 Record 时键已知改具名字段类、键不固定用 Map，不改成 [key: string] 索引签名｜读到：规范或返修派工要求去掉 Record<K, V>（原文可能是「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」）；写错：把 Record 改成 interface X { [key: string]: T } 索引签名（编译报 arkts-no-indexed-signatures），用到的地方还写 obj['key']（报 arkts-no-props-by-index）
- rule-a25cc746061a｜查询参数让请求工具收 Map<string,string> 或参数类，不加索引签名适配 Record 形参｜写错：为适配 `Record<string, string>` 形参给参数类加 `[key: string]: string`，或把 `Record` 字面量写成标识符键 `{ page: '1' }`、改成带 `Record<string, string>` 注解的变量仍是标识符键
- rule-403f41bbd4c3｜构造 Record<string, Object> 时先建空字典再下标赋值，不写标识符键的对象字面量｜读到：工程里已编译的写法和模型模板用 const x: Record<string, Object> = {} 再 x['key'] = v，或 { 'id': this.id as Object } 这种字符串键；写错：写成 const x: Record<string, Object> = { key: value, … }、toJson() 里 return { key: this.key, … }，或把内联的 { x: …, y: … } 当 Object 值嵌进去
