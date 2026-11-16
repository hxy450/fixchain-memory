# 状态接口表里与通用属性同名的成员

agent 会看到什么：读到源端事件或模型字段叫 position、duration 之类（如播放进度事件的 position），要转成组件状态；规格的「@Local 变量」状态接口表直接沿用源字段名，写出 position / width / height / id / visibility / enabled / zIndex / opacity 这类与通用属性同名的成员

## 规矩

- rule-81efced3763f｜规格的「@Local 变量」表里成员名与 position 等通用属性同名时改名，并写出与源字段的对应｜读到：源端事件或模型字段叫 position、duration 之类（如播放进度事件的 position），要转成组件状态；写错：规格「@Local 变量」状态接口表直接沿用源字段名，写出 position / width / height / id / visibility / enabled / zIndex / opacity 这类与通用属性同名的成员
