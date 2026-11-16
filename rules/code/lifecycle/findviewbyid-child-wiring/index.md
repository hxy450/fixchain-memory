# onCreate 里 findViewById 后对子 View 的接线

agent 会看到什么：读到 Activity.onCreate 里 findViewById 取到自定义 View 后立即调它的 setter（设状态、设触摸监听）、只接线一次；产物里宿主在 NavDestination.onReady 或 init 里读子组件 aboutToAppear 登记的句柄、用 ?. 调实例接线，或注释断言 onReady 时句柄必已就绪

## 规矩

- rule-00e7188e7109｜源端 onCreate 里 findViewById 后立即调 setter 时，目标在子组件登记时回调宿主完成接线｜读到：Activity.onCreate 里 findViewById 取到自定义 View 后立即调它的 setter（设状态、设触摸监听）；写错：子组件 aboutToAppear 只把自身写进宿主传入的句柄、不回调宿主，宿主在 NavDestination.onReady 里读句柄后接线
- rule-ae367920d72b｜只执行一次的接线点不用 ?. 静默跳过，取不到实例时由登记回调补接或打错误日志｜读到：源端 onCreate 里 findViewById 后只接线一次；写错：一次性的初始化（onReady、init）里用可选链 ?. 调子组件实例的 setter，实例为 null 时静默跳过、之后再无接线点
- rule-6297b8aa8612｜依赖宿主生命周期回调和子组件创建的先后时，照 d.ts 注释写，没核实就按与先后无关设计｜读到：源端在 onCreate 里用 findViewById 同步拿到子 View 引用；写错：注释写「句柄登记于子组件 aboutToAppear，onReady 时必已就绪」「页面 onReady 后注入」这类没核实的先后断言
