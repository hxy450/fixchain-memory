# 源端渲染线程在页隐藏时会拿到空画布，目标在 onPageHide 让画布失效、onPageShow 重走创建

审的是：代码
触发（任一种）：
- 读到：Thread 子类 run() 里 lockCanvas() 后直接绘制不判空；surfaceCreated 里直接 thread.start()；configChanges 不含 orientation；写错的样子：目标只在 aboutToDisappear 里停掉帧循环（clearInterval）、丢弃迟到回调，没有 onPageHide 处理（切后台回来循环照跑）；方向变化时无条件关弹窗、重开
适用范围：SurfaceView 加自建渲染线程的游戏或动画页迁成 ArkUI 页面加 Canvas 帧回调，目标页面隐藏、旋转时不重建时
做法：
- onPageHide 里让画布失效并通知仍在跑的循环，下一次迭代拿到空画布，走源端同样的结果；onPageShow 里清画布后重走源端 surfaceCreated 的逻辑，异常只记日志
- 窗口方向变化时分支：循环在跑就走画布失效；已结束就清掉对话框，按新几何重建视图（新位图、新循环）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onPageHide 走画布失效、onPageShow 清画布再走 surfaceCreated、方向变化按循环是否在跑分支后，与安卓实测结果一致：修复后保留的写法，对应源端崩溃与重建的可观察结果，不是额外防护（出处：卡里修好并验证过）
- onPageShow?(): void / onPageHide?(): void：页面每次显示 / 隐藏时调用，含切前台 / 切后台；只对 @Entry 装饰的组件生效：切后台、回前台的挂点（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomComponent.onPageShow、CustomComponent.onPageHide）
- on(type: 'add' | 'remove' | 'change', callback: Callback<number>): void：display 的变化监听，可在 change 里比较 rotation 判断方向变化（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.on）
未核实：目标页若是 NavDestination 而非 @Entry 页面，onPageShow / onPageHide 不触发，要换成 NavDestination 的显示隐藏回调；卡里是 @Entry 页面
来源：1 张卡，1 个应用
- case-d3f1bcc562a64e5f56f7（Bubble Shooter）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断
