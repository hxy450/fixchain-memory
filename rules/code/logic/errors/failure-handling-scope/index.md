# 源函数的失败处理范围：try/catch 和 Either 的 Left

agent 会看到什么：读到源端辅助函数内部自带 try/catch 只记日志、循环里不逐条 catch、chunked(N).forEach 忽略单批失败，或调用链用 .onLeft { Log.e(…) } 消费 Either / Result 的失败；产物里 catch 包的范围、continue / return 和对返回值的处理和源端不同

## 规矩

- rule-a7a3484e94f8｜逐个对照源函数的 try/catch 作用域，保持相同的中断和继续语义｜读到：源端辅助函数内部自带 `try { … } catch (e: Exception)`（失败只记日志）；写错：目标辅助函数没有内部 `catch`，异常冒泡到调用方，调用方后续的持久化（如 hash 落库）被跳过
- rule-2f46601f850a｜回填返回 Either 或 Result 的调用时，按源端 onLeft 消费返回值，不只 await｜读到：Kotlin 调用链 `.onLeft { Log.e(TAG, "… ${it.code}, ${it.body}") }`；目标签名返回 Promise<Either<错误, 结果>>；槽位注释写「Left 错误只记录」；写错：只有一行 await 调用、不接返回值，Left 分支没有任何 hilog.error / console.error 日志
