# View.invalidate 的重绘请求和帧调度

agent 会看到什么：读到自定义 View 在 onDraw 尾部 invalidate() 自续帧、业务层用 invalidate() 请求重绘；产物里另有直调 render() 的入口、用 setInterval 排帧又不清句柄，或请求重绘后立刻把渲染器字段镜像到 @State / @Local

## 规矩

- rule-0ca93517f70d｜移植 View.invalidate 自续帧时，写成待决标志合并、postFrameCallback 只绘一次的唯一入口｜读到：自定义 View 的 onDraw 尾部在动画进行时调 invalidate() 再 tick() 自续帧，业务层也用 invalidate() 请求重绘；写错：目标渲染器另有同步直调 render() 的公开入口（方法体只有 this.render()），引擎桥、尺寸变化、onDraw 尾部各走各的路径；或者没有待决标志，同一帧的多次请求各排一次
- rule-cca10e457ca4｜帧调度用定时器时写一次性的 setTimeout；用 setInterval 就由同一句柄 clearInterval｜读到：源端 onDraw 尾部的 invalidate() 每次只请求下一帧一次 onDraw；写错：帧调度写成 setInterval(…, 16)，回调里只把句柄变量复位（如置 -1）、不调 clearInterval，随后绘制尾部又开新的 setInterval
- rule-637b5396d191｜依赖绘制结果的状态在使用时直读渲染器字段，不在请求重绘后立刻镜像｜读到：源端在 onDraw 里算出的状态（如某个按钮是否可用）存在 View 字段里，事件处理时直接读；写错：页面调用渲染器的重绘请求后，立刻把渲染器字段复制到 @Local 或 @State 镜像变量，后续逻辑读镜像
- rule-7c4b72fe34ba｜源 tick 随 onPause/onResume 启停时，覆盖层定时器跟随暂停恢复，不只绑组件挂载卸载｜读到：源自绘 View 的 onPause 里 handler.removeCallbacks(tick)，onResume 里 tick.run()；写错：setInterval 只在 Canvas 的 .onReady(...) 里启动、只在 aboutToDisappear 里 clearInterval，切后台或进设置页仍按周期绘制
- rule-382218e6f18d｜源 onPause/onResume 里启停自绘 View 的 tick 时，目标引擎向覆盖层发启停通知｜读到：源预览类的 onPause / onResume 里调用自绘 View 的 onPause() / onResume()（移除或重启 tick）；写错：目标引擎的 onPause / onResume 只调预览 surface 的空 onPause / onResume，没有通知覆盖层停止或重启绘制
- rule-8789d0e85449｜覆盖层用 setInterval 代替源端 tick 时，每个 tick 先判暂停、再调引擎逐帧钩子、最后绘制｜读到：源 onDraw 里先判暂停，再做对焦框过期复位等逐帧处理，最后分发绘制回调；写错：覆盖层 setInterval 回调里的绘制函数没有暂停守卫，也不调用引擎的逐帧钩子，只自己绘制
- rule-1ad701215574｜引擎承接源端逐帧分发时，逐帧钩子要有调用方或 FWD-REF 登记，驱动源先核实｜读到：源自绘 View 用 Handler.postDelayed 循环 invalidate，onDraw 里依次做暂停判断、过期复位、逐帧分发；spec 把这条 AC 指向覆盖层的逐帧入口；写错：引擎里写了逐帧钩子，注释称由 XComponent 帧率或 frameStart 驱动，但 grep 钩子名只有定义、没有调用方，registry 里也没有 FWD-REF / HANDOFF
