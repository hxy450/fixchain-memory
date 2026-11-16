# 计时 API 的映射

agent 会看到什么：源端用 System.nanoTime() 做动画或帧计时；规格实现映射里写的目标计时 API（如 performance.now）和「行为等价」「低难度」标注

## 规矩

- rule-f4624f179112｜规格给 System.nanoTime 等计时 API 写映射时，写明所需语义并以 SDK 声明为目标 API 的证据｜读到：源端用 System.nanoTime() 做动画或帧计时；写错：规格的实现映射写「System.nanoTime() → performance.now()（ms）」并标「低难度 / 行为等价」，没写单调、是否含深睡眠、精度这些语义，也没有引用 SDK 声明证明目标 API 存在
