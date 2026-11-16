# 分支、异常与集合

读到 catch 后返回、提前 return、零分母和钳制保护、HashSet / HashMap 遍历、由不同调用点传入的一组常量、克隆的命名和内容、没捕获的异常退出，规格的 AC 或映射表写这些分支和顺序时

## 触发族

- [源码里 catch 异常和提前 return 的边界分支](catch-early-return-branch/index.md)（5 条）：源码的结果由 catch（NullPointerException、OutOfMemoryError）后返回、提前 return 或未加括号的 &&/|| 混排决定，规格的 AC 或映射表按注释、通用语义概括，或另加了源端没有的预检
- [源端辅助方法里的边界保护（零分母、钳制、空集合）](boundary-guards/index.md)（1 条）：读到源端辅助方法里有 if (total == 0)、coerceIn / clamp 或空集合判断；源码理解笔记只记了构造和调用接线，没记这些边界
- [由不同调用点传入的一组来源常量](constant-domain-callers/index.md)（2 条）：读到源端一组来源常量（如几种检测触发来源）分别由不同调用点传入同一个业务方法；AC 只写「N 种场景分别传对应值」，没写每个取值由谁在什么条件下传入
- [HashSet / HashMap 遍历决定的输出顺序](hash-iteration-order/index.md)（1 条）：读到 Java 源码用 HashSet / HashMap 收集后经 keySet()、toArray()、new ArrayList<>(set) 遍历，结果决定输出内容或尝试、写入顺序；AC 只写「去重」，或写成插入序、以「本来无序」略过
- [克隆操作的名称变换和内容来源](clone-name-content/index.md)（1 条）：读到源码或分析参考里克隆名用后缀格式化原名、克隆内容取编辑草稿和重排后的子项；验收项只写「duplicates fields … with new IDs」
- [照源保留的崩溃退出](keep-crash-exit/index.md)（1 条）：源端有会抛未捕获异常的路径（整数除零、数组负下标）且没有 setDefaultUncaughtExceptionHandler；规格里「照源复刻崩溃」的条目和 errorManager.on('error') 既定项并存
- [接口实现类覆写的一组 on* 回调](override-callback-set/index.md)（1 条）：读到源端接口实现类继承各回调都是空默认实现的基类，在一段连续区域 @Override 多个 on 开头的错误、信息回调（各自 showToast 本地化提示）；规格的服务层清单和 AC 只列了其中几个回调，其余的既无清单项也无 AC
