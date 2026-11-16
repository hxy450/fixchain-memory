# 帧调度用定时器时写一次性的 setTimeout；用 setInterval 就由同一句柄 clearInterval

审的是：代码
触发（任一种）：
- 读到：源端 onDraw 尾部的 invalidate() 每次只请求下一帧一次 onDraw；写错的样子：帧调度写成 setInterval(…, 16)，回调里只把句柄变量复位（如置 -1）、不调 clearInterval，随后绘制尾部又开新的 setInterval
适用范围：ArkUI 自绘视图的帧调度没有用 UIContext.postFrameCallback、改用定时器时
做法：
- 首选 uiContext.postFrameCallback 对齐 vsync；只能用定时器时写 setTimeout(cb, 16) 做一次性调度
- 若用 setInterval，回调完成或停止时调 clearInterval(同一个返回值) 再复位句柄；不在回调里只复位 id 后再开新定时器
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setInterval(handler: Function | string, delay: number, ...arguments: any[]): number；只能调 clearInterval 手动删除：重复定时器，不清就一直触发（出处：鸿蒙 SDK 的 ets/api/@internal/full/global.d.ts，setInterval）
- setTimeout(handler: Function | string, delay?: number, ...arguments: any[]): number；回调执行后自动删除：一次性定时器（出处：鸿蒙 SDK 的 ets/api/@internal/full/global.d.ts，setTimeout）
- clearInterval(intervalID?: number): void；不传 ID 时不取消任何定时器：取消 setInterval 返回的那个定时器，要在创建它的线程里删（出处：鸿蒙 SDK 的 ets/api/@internal/full/global.d.ts，clearInterval）
来源：1 张卡，1 个应用
- case-569a68ae79caad45dbb6（2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
