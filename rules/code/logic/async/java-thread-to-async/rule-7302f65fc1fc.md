# 把同步的「提交后清空挂起状态」移植到 async 时，先摘下挂起对象再 await

审的是：代码
触发（任一种）：
- 读到：源端 Java 在调用线程上同步提交或保存挂起对象后把挂起字段置空（`字段 = null`）；写错的样子：ArkTS 里先 await 提交或保存的调用，之后才把挂起字段置空（this.pending = null）
适用范围：把 Java 同步执行的「提交挂起对象后清空」移植成 async/await 时
做法：
- 先摘下再等待：const req = this.pending; this.pending = null; await this.submit(req)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 提交在队列满时 await 让出事件循环，等待期间新建的批次会被随后的置空清掉；改为 await 前摘下后，新批次不再被清：await 之后清空会误伤新状态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4171cd43bbb420b4ee40（opencamera-hmos）：做法第 1 步 ← 建议 6、诊断；取值 1 ← 诊断
