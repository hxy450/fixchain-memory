# 网络回调里信封成功和 data 层错误码的判别

agent 会看到什么：读到源端网络回调先按信封 isSuccess 分流、再在 data 层用 optInt("errorCode") / optBoolean / has("…") 判别；产物里回调用服务层解析出的 report.success / report.errorCode 分支

## 规矩

- rule-e179fe81e9b2｜修补回调分支的文案或常量前，按源端完整判别路径逐层对照分支结构｜读到：源端网络回调先按信封 isSuccess 分流，成功分支里再按 dataObj.has("…") 分流，错误码和附带标志用 data 层的 optInt("errorCode") / optBoolean(…) 读，位于成功分支的 else 里；写错：目标把同名错误码判断放在 if (report.success) {…; return} 之后（成功分支之外），修补时只改了文案或常量，结构没动
- rule-0ed4a5eb80cf｜目标回调用服务层解析出的 success/errorCode 时，核对解析函数的读取层级和缺省值｜读到：源端从 data 层读错误码和标志（dataObj.optInt("errorCode")、optBoolean(…)），信封成功另由外层字段判定；写错：服务层解析函数从 root 层读 errorCode，success 由网络码和 root.code（带缺省值）组合产出，回调直接用 report.success / report.errorCode，复核结论写「逐行一致」却没打开解析函数
