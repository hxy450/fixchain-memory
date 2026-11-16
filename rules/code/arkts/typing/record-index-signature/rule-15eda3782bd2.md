# 按规范去掉 Record 时键已知改具名字段类、键不固定用 Map，不改成 [key: string] 索引签名

审的是：代码
触发（任一种）：
- 读到：规范或返修派工要求去掉 Record<K, V>（原文可能是「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」）；写错的样子：把 Record 改成 interface X { [key: string]: T } 索引签名（编译报 arkts-no-indexed-signatures），用到的地方还写 obj['key']（报 arkts-no-props-by-index）
适用范围：项目规范禁用 Record、返修时替换键值集合的类型声明
做法：
- 键集合已知就改成具名字段类（每个键一个带类型和默认值的字段），访问写 obj.field
- 键不固定就用 Map<K, V>，用 get / set 访问
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- arkts-no-indexed-signatures（错误码 10605017）：ArkTS不允许index signature：[key: string] 索引签名和 Record 一样过不了（出处：typescript-to-arkts-migration-guide.md，不支持index signature）
- arkts-no-props-by-index（错误码 10605029）：只能 obj.field，不支持 obj['field']：改成具名字段类后，调用处的下标访问也要改成点访问（出处：typescript-to-arkts-migration-guide.md，不支持通过索引访问字段）
- 官方适配案例对 index signature 的建议改法是 Record<string, string>：Record 本身 ArkTS 允许；去掉它是项目规范的要求（出处：arkts-more-cases.md，arkts-no-indexed-signatures）
- 改成只含已知键的具名类、五个具名字段的设置类后编译通过：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 这个键值集合的键是不是固定的一组：源工程里写入这个集合的 Kotlin 代码（DataStore 键、偏好键常量），以及目标工程里读它的地方；列出所有出现过的键；全部是常量就写具名字段类，有运行时拼出的键就用 Map
来源：1 张卡，1 个应用
- case-98e7bd27bb334db83f51（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 4 ← 诊断
