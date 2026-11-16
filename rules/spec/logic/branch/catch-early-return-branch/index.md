# 源码里 catch 异常和提前 return 的边界分支

agent 会看到什么：源码的结果由 catch（NullPointerException、OutOfMemoryError）后返回、提前 return 或未加括号的 &&/|| 混排决定，规格的 AC 或映射表按注释、通用语义概括，或另加了源端没有的预检

## 规矩

- rule-1ae4d7d1e9d7｜源码条件含 &&/|| 混排、未赋值元素或提前 return 时，AC 按源码实际结果写｜读到：Java 源码里有未加括号的 `a && (…) || (…) || (…)` 混排、数组元素没赋值就使用（NullPointerException 被 catch 后返回 false）、格式错误时 Toast 后提前 return 的分支；写错：AC 按注释或通用真值表概括（如「三组态真值归某功能」「HashSet 语义去重」「响应式等价」），没有源码锚点、触发条件和原结果
- rule-a8ab77e35953｜源端只在 catch(OutOfMemoryError) 时报文件过大，规格写照常读取、捕获分配失败再提示｜读到：源码只在 catch (OutOfMemoryError) 里提示文件过大，读之前没有任何大小阈值；写错：映射表写成「读前长度预检（超阈值拒读并提示文件过大）+ try/catch 兜底」，并以「纯语言构造」为依据新增大小上限
- rule-a169520d9fd6｜源码注释说无匹配交给常规路由时，规格只按实际判断写跳转门槛，不加注册路由过滤｜读到：源端深链处理只有 `if (x)` 真值判断就 `history.push(...)`，旁边注释写 'If no match, do nothing - let regular routing logic take over'；写错：规格的验收条目写「为空或未注册路径 → 不 push，resolve 返回 null」，在解析函数里新增注册路由过滤
- rule-4102bbd7e2ec｜转写源码错误处理分支时，AC 按运行时会抛的异常和实际结局写，不写成兜底继续｜读到：Java 源码只 `catch (IOException e)`，try 里却有 Gson 解析（抛 JsonSyntaxException）；`findFile(...)` 的返回值直接 `.exists()`；`R.string.x + ": " + e.getMessage()` 把资源 int 与字符串相加；写错：AC 写「读取/解析失败兜底：返回空对象（不崩溃），任务继续处理其余文件」「目录缺失整体返回 false，进程不崩溃」「不复制崩溃行为」「源码现状兜底」，或把资源 id 拼接写成文案拼接，且没有引 PD-/D- 决策 ID
- rule-4c2d57ec4bdb｜规格总结源端循环的错误处理时，把抛异常和返回 null 分开写传播范围｜读到：源端循环里有一步可能抛异常（如解密）且没有逐条 catch，异常落到外层 catch；另一步返回 null 时推进游标并 continue；写错：验收条目把「解密失败 / 解析为 null」合并成同一个 continue 分支，写「推进时间戳、不中断整批」
