# 资源文件名和 element name 里的非法字符

agent 会看到什么：源 res 来自 apktool 反编译，drawable 里有 $<父名>__N 内联片段；产物 resources 下 media 文件名或 element 的 name 含 $、-、. 等 [a-zA-Z0-9_] 以外的字符，构建报 Invalid resource name

## 规矩

- rule-92a149b67483｜反编译 res 里的 $父名__N 内联片段先按父资源分类处理，不按原名输出成 media｜读到：apktool 反编译 APK 的 res/drawable 里有 `$<父名>__N.xml` 文件（aapt 从 animated-vector、animation-list、selector 等拆出的内联片段）；写错：base/media 下出现 `$` 开头的文件（如 `$…__0.svg`），其中有带库前缀（avd_、m3_、mtrl_、abc_）的父资源片段没被跳过
- rule-0708738d6368｜资源写完交构建前，对输出目录里每个 media 文件名和 element name 校验 [a-zA-Z0-9_]｜写错：resources 下 media 文件名或 element 的 name 含 `$`、`-`、`.` 等 [a-zA-Z0-9_] 以外的字符；复查只看了转换失败清单，没看输出目录
