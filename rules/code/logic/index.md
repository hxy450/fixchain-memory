# 业务逻辑与源码语义

源端有 Java / Kotlin 的分支条件、回调分支、提交前校验、ViewModel 方法在请求前后的步骤、工具类静态入口起的业务链、数值运算、集合遍历、异常捕获、协程并发、字符串和字节处理、日期计算，目标端有照着移植的 TS 业务代码时

## 子主题

- [异步与并发](async/index.md)（15 条）：源端有 viewModelScope.launch、多路请求和缓存、Mutex.withLock、Executors 单线程执行器、Thread 轮询重连循环，目标端有 Promise、async / await、请求取消和排队时
- [集合与顺序](collections/index.md)（14 条）：源端有 HashSet / HashMap 遍历、addAll、按下标赋值、按引用原地改写数组、filter / sortedBy / Comparator 排序，目标端有 Set、Map、find、slice、.sort 时
- [日期和时间](datetime/index.md)（11 条）：源端有 Calendar、SimpleDateFormat、时区和周的计算、System.nanoTime、农历算法库，目标端有手写的日期拆分、时区偏移和时钟函数时
- [异常与日志](errors/index.md)（17 条）：源端有 try/catch 按异常类或消息分流、Log.e / Log.w、会抛错的异步初始化，目标端有 catch 的范围、Promise 的 .catch、console.error / hilog 时
- [数值运算](numeric/index.md)（13 条）：源端有 (float) 强转和 f 后缀字面量、Float 相等比较、算式里的倍率和偏移、超出 2^53 的 long 常量、模型字段的时间单位，目标端有 TS 的算式和数值常量时
- [字符串、字节与编解码](strings/index.md)（36 条）：源端有 BufferedReader.readLine、String.split / trim、android.util.Patterns、byte[] 字面量、substring 下标、proto 字段的 varint / fixed32，目标端有 split、TextDecoder、RegExp、Uint8Array 和手写的 codec 时

## 触发族

- [源端的分支条件和执行时机](source-branches/index.md)（9 条）：读到源端 switch 只列几个失败码、if 守卫没有 else、成功分支先 close() 再 Toast 和 finish()、只在特定方法里重建列表，或有看似缺陷的可观察行为；产物里改成 !== 0、新增清空分支、调了先后、改成渲染时派生，或注释里自定「缺陷不移植」
- [源 ViewModel 方法在请求、提交前后的步骤](viewmodel-steps/index.md)（5 条）：读到源 ViewModel 的方法在请求前查库回填参数、提交时先经 Repository 写入、推进后预取图片，或在弹层 onExpanded 时才加载，交回的代码少了这一步或换了调用时机（只 showToast、直接用传入对象的字段、页面初始化就请求）
- [工具类静态入口起的业务链](static-entry-chain/index.md)（2 条）：读到工具类静态方法或 companion object 直接起链（先弹 loading 的 Dialog、下载、导出文件）；产物里 static 入口的签名带没带 context 和回调，直调入口有没有真的调用服务并在终态收口
- [带结果回调的拦截和分支](callback-branches/index.md)（2 条）：源端回调按 result.on(true) 继续、result.on(false) 中止（如登录拦截后续做原操作）；产物里拦截处只 return 中止，或注释写「对齐源端回调」却少了分支
- [提交方法开头的参数校验](submit-precondition/index.md)（1 条）：读到 ViewModel 的提交方法开头校验参数、选项为 null 即提示失败并返回；产物里的前置判断在「未选」之外多了 .length > 0 一类条件
- [Kotlin 的 when 分支和 ?: 回退链](kotlin-when-elvis/index.md)（4 条）：读到 Kotlin 源码里 when / in setOf(...) 按一组常量分支、a ?: b ?: 常量 的回退链（含 StateFlow 初值里先解析持久值再回退）；产物里 TS 的 if / switch、?? 链和 !== 组合少了链上某一步、漏了页面上看不到的取值，或回退只写在设置方法里
- [应用接口的 on* 错误回调和它们的提示](interface-error-callbacks/index.md)（2 条）：读到源实现类 @Override 基类（空默认实现）的多个 on* 错误回调、各自 showToast(R.string.…)，或操作的 errorCallback 只转给应用接口的错误回调；产物里子类只覆写规格点名的几个 on*、其余继承空实现，或页面桥的失败回调直接 showToast 资源键字面量
- [能力门函数（supports…）的多重条件](capability-gate-conditions/index.md)（2 条）：读到源端 supports… 一类能力门函数用 && 连着几重条件（是否由拍照 Intent 启动、大堆内存阈值、陀螺仪是否存在、预览能力）；产物里的能力判断少了条件、用 canIUse('SystemCapability.…') 设备能力位代替，或契约里缺判断入口时写成恒 false 删掉这条
- [依赖库里取不到源码的类、方法和常量](library-without-source/index.md)（6 条）：读到源码 import 或 extends 依赖库（aar / jar，如粒子库的 Party、Emitter，库里的 Pattern 常量）里的类和方法而源码树里没有它的定义，规格可能要求行为等价；产物里自研的等价组件、正则或算法按配置面、记忆、单测或 AC 反推，注释写「库无源码」「不可核」「风险低」，没有 FWD-REF 和缺口登记
- [回调接口实现类覆写的回调](callback-impl-overrides/index.md)（1 条）：读到源端回调接口的实现类 @Override 了一组回调；产物里实现类 extends 回调全是空默认的 Basic 基类、没覆写源端覆写过的回调，VM 上承接这些回调的方法没有调用者
