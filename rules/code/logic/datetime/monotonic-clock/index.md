# System.nanoTime 一类的单调时钟计时

agent 会看到什么：读到源端用 System.nanoTime() 求帧间隔、推进动画进度或重置计时基线；产物里的时钟函数写成 performance.now()、Date.now() 或 systemDateTime.getTime()，注释写「ms 墙钟」

## 规矩

- rule-5906560b9eba｜System.nanoTime 计时用 getUptime(TimeType.ACTIVE)，不换成墙钟｜读到：源端用 System.nanoTime() 求帧间隔、推进动画进度或重置计时基线（单调纳秒时钟）；写错：目标的时钟函数里写 performance.now()（ArkTS SDK 里没有，编译报找不到符号或 Kit 无导出），或者改成 Date.now() / systemDateTime.getTime()，注释写「ms 墙钟」
