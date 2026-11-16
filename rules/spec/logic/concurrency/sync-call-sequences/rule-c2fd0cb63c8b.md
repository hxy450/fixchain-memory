# 规格接口清单不照搬 Java 的 void，阻塞等待的方法写成 Promise<void> 并在验收写明需 await

审的是：规格
触发（任一种）：
- 读到：源方法是 void 但内部阻塞等待队列、线程或 IO 完成，验收里有「X 先于 Y」的排序要求；写错的样子：规格接口清单照搬 Java 签名写成 xxx(): void，没标出 ArkTS 里它必须是可 await 的 Promise；验收没写调用方需 await
适用范围：规格里写接口清单和排序类验收条目的那几节
做法：
- 接口清单里把阻塞等待的方法和依赖它的方法写成 `(): Promise<void>`，验收条目写明调用方需 await 后再执行后续动作
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- E take() throws InterruptedException：取队头，必要时等到有元素：源端 BlockingQueue 消费是阻塞等待，翻成 ArkTS 只能是 Promise（出处：java.util.concurrent.BlockingQueue#take）
来源：1 张卡，1 个应用
- case-742303a1abdd7ba274ec（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断
