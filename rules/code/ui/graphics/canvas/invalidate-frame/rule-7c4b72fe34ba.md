# 源 tick 随 onPause/onResume 启停时，覆盖层定时器跟随暂停恢复，不只绑组件挂载卸载

审的是：代码
触发（任一种）：
- 读到：源自绘 View 的 onPause 里 handler.removeCallbacks(tick)，onResume 里 tick.run()；写错的样子：setInterval 只在 Canvas 的 .onReady(...) 里启动、只在 aboutToDisappear 里 clearInterval，切后台或进设置页仍按周期绘制
适用范围：Canvas 自绘覆盖层的定时器生命周期
做法：
- 收到暂停通知时 clearInterval(<定时器 ID>)，恢复时重新 setInterval；绘制入口再判一次暂停
- aboutToDisappear 只清本组件持有的资源，启停不靠组件挂载和卸载
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- clearInterval(intervalID?: number): void：取消 setInterval 设的重复定时任务，传 setInterval 返回的 ID（出处：js-apis-timer.md，clearInterval）
- 覆盖层经引擎生命周期监听启停 tick，绘制入口再判一次；aboutToDisappear 只清本组件持有的回调：修好后的写法，暂停态不再绘制（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-74192ad19ea88a31750b（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 诊断；取值 2 ← 诊断
