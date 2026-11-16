# 源端 Crouton.makeText(…).show() 迁成全局单例队列加宿主组件，并提供 cancelAll

审的是：代码
触发（任一种）：
- 读到：源端调用 Crouton.makeText(activity, message, style, 容器 ViewGroup).show()，带容器句柄；写错的样子：目标端是页面自持、@Param visible 驱动的单条提示组件，没有队列和 cancelAll，隐藏延迟只用 duration；或映射成 promptAction 的 Toast
适用范围：把 crouton 这类带队列语义的提示条库迁到 ArkUI 时
做法：
- 写一个全局单例管理器：静态队列串行显示，一条显示 duration 加进入动画时长后开始退出，退出动画结束再放下一条；提供 cancelAll 清空队列并移除当前条
- 在页面顶层 Stack 里放一个宿主组件，订阅管理器并渲染当前条；调用处改成向管理器入队
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- crouton 1.8.5：Manager 单队列串行、(duration + inAnimation) 后移除、out 动画后放下一条、cancelAllCroutons、不拦截触摸：返修解包后照着重写的库语义：静态队列 + 宿主组件，延迟为 duration + 进入动画（出处：卡里修好并验证过）
针对本应用要查的：
- 进出动画的时长和曲线：源工程里 Configuration.Builder 的 setInAnimation / setOutAnimation 引用的 res/animator/ XML；读 android:duration 和 android:interpolator，作为宿主组件的进出转场参数
未核实：卡里的环境是 HarmonyOS 6.1.1（API 24），本机是 API 23
来源：1 张卡，1 个应用
- case-cfa31a0f8f73caf9c2ab（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断
