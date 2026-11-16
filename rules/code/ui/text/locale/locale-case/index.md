# 大小写转换和区域标签

agent 会看到什么：读到源端判定函数里 lowercase(Locale.ROOT) 后再比对，或按资源的 locale 做 textAllCaps / toUpperCase；产物里谓词内部直接 === / Set.has 比较，或把 getConfigurationSync().locale 原样传给 toLocaleUpperCase

## 规矩

- rule-cfd1d5a4ae41｜源端判定函数内部先 lowercase 再比对时，目标的名称谓词也在内部先 toLowerCase｜读到：源端判定函数内部先对名称做 lowercase(Locale.ROOT)（或 toLowerCase(Locale.ROOT)），再和小写字面量或集合比较；写错：目标改写出的名称谓词内部直接用 === 或 Set.has 比较小写字面量，大小写归一只放在调用方的 name.toLowerCase() 里
- rule-05783c85ed3c｜资源 locale 转 BCP 47 时按 '_' 拆分、丢空子标签再用 '-' 连接，失败回落｜写错：把 resourceManager.getConfigurationSync().locale 直接传给 toLocaleUpperCase，或写成 locale.replace(/_/g, '-')，没处理空子标签，也没有 RangeError 回落
