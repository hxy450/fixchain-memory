# 目标回调用服务层解析出的 success/errorCode 时，核对解析函数的读取层级和缺省值

审的是：代码
触发（任一种）：
- 读到：源端从 data 层读错误码和标志（dataObj.optInt("errorCode")、optBoolean(…)），信封成功另由外层字段判定；写错的样子：服务层解析函数从 root 层读 errorCode，success 由网络码和 root.code（带缺省值）组合产出，回调直接用 report.success / report.errorCode，复核结论写「逐行一致」却没打开解析函数
适用范围：目标端回调不直接读响应 JSON、而是依赖单独解析函数产出的字段时
做法：
- 同时打开解析函数，逐个字段核对读取层级（root 还是 data）和缺省值，对齐源端的读取层级和 optInt / optBoolean 的缺省（0 / false）后，再给「逐行一致」的复核结论
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- JSONObject#optInt(name) 缺键返回 0；optBoolean(name) 缺键返回 false：解析函数里对应字段的缺省值要和这个一致（出处：org.json.JSONObject#optInt、#optBoolean）
针对本应用要查的：
- 源端每个字段从哪一层读：源工程这个回调所在的 Java 方法里 new JSONObject(…)、optJSONObject("data") 之后各 opt* 调用的接收者；接收者是根对象就是 root 层，是 data 对象就是 data 层；解析函数按同一层读
来源：1 张卡，1 个应用
- case-5b91aeeca2e493368af0（企业安全培训）：做法第 1 步 ← 建议 3、诊断
