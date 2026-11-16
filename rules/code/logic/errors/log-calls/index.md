# 新写或改写的日志调用

agent 会看到什么：源端 Log.e / Log.w 或静默吞错的 catch，工程已有 hilog 写法；产物里 catch 和边界处新写的 console.error / hilog 调用缺定位字段或带了敏感内容

## 规矩

- rule-4fd4c7651609｜catch 里新增错误日志时沿用工程的 hilog 写法写 hilog.error，不写 console.error｜读到：源端 Kotlin runCatching { audioTrack.stop() } 之类静默吞错、没有 Log 调用；工程里已有 import { hilog } from '@kit.PerformanceAnalysisKit' 和 TAG、DOMAIN 常量；写错：服务层或 ViewModel 的 catch 里新写了 console.error(`… ${error}`) 或 console.log(...)
- rule-7645dfd37c60｜改写台账点名边界上的日志调用时，补上类型、阶段、耗时等定位字段并脱敏｜写错：改写后的失败日志只有一句文字加 error.message，或网络诊断只有 method、statusCode、durationMs，缺类型、阶段、失败分类、数量；或者把 token、ID、正文、完整请求/响应写进日志
