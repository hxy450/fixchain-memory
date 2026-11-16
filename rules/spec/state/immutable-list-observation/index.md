# 整体替换的列表和订阅队列（copy、StateFlow.update）

agent 会看到什么：读到源端用 data class copy 替换列表项、StateFlow.update { list + item } 生成新列表、宿主订阅队列；规格把「map + copy」「尾拼接」当照搬写法，没写 ArkUI 端行内字段变化靠什么被观察、队列消费方靠什么触发

## 规矩

- rule-3ae83b89b83d｜规格写可变列表或订阅队列时，把 ArkUI 端的变更写法和观察方式成对写明｜读到：源端用 data class copy 替换列表项、StateFlow.update { list + item } 生成新列表，宿主订阅队列；写错：规格把「map + copy 只替换目标行」「尾拼接」当作照搬的写法，写了 key=id 和「@Trace 数组驱动刷新」，却没写行内字段变化靠什么被观察、订阅队列的消费方靠什么触发
