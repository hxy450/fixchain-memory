# Moshi 等解析器解析失败时的结果和错误类型

agent 会看到什么：读到源端用 Moshi 严格反序列化（缺字段、类型不符抛 JsonDataException），或用一次 Either.catching(onCatch = …) 包住 XML、JSON 全部格式的解析；产物里 fromJson 给缺字段填默认值、坏响应当空结果，或 catch 里按格式分出不同的错误 kind

## 规矩

- rule-58b6e20fb23f｜复用缺字段填默认值的 fromJson 且结果要全量替换本地表时，先严格校验｜读到：源端用 Moshi 严格反序列化响应（缺字段或类型不符时失败），结果全量替换本地表（如设备列表）；写错：目标直接用会给缺失字段填默认值的 DTO fromJson，坏响应被当成空列表，清空了本地表
- rule-2c899b5970fe｜源端一次 Either.catching 包住全部格式解析时，JSON 解码失败也返回同一个错误类型｜读到：源端解析入口用一次 Either.catching(onCatch = 某解析错误) 包住 XML、JSON 等全部格式；sealed class 里另有一个 JSON 专用的错误类型，但这条路径不产生它；写错：目标解析的 catch 里按格式分支，为 JSON 格式单独返回 JSON 专用的错误 kind；文件头注释写「XML/JSON 解码失败 → 两种错误」
