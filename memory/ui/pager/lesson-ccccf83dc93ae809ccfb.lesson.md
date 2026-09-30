# 分页容器的初始页用 Swiper.index 状态绑定，不在 onReady 里立即调用 changeIndex

ID：`lesson-ccccf83dc93ae809ccfb` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把源端 ViewPager 的初始定位（post 里 setCurrentItem）与首播触发转写成 ArkUI Swiper 时

## 适用情境

源端装好数据后在 view.post 等延后回调里 setCurrentItem(index, false)，并靠 onPageSelected 启动当前页；目标在 NavDestination.onReady 读路由参数，Swiper 位于按列表非空条件渲染的分支里。

## 原因

在 onReady 同一回调里先给列表赋值、再立即调用 SwiperController.changeIndex 时，Swiper 还没挂载，命令被静默丢弃，始终停在第 0 页；源端 post 的延后语义没有落实。

## 做法

1. 路由参数先写入响应式状态，再用 Swiper.index(state) 声明式绑定初始页。
2. 转写 post、doOnLayout 等延后回调时，写明回调执行时哪个组件必须已挂载；容器依赖同一回调里刚赋值的数据才会创建时，它的 controller 此时尚未生效。
3. 源端首播依赖选页回调时，目标对初始项显式调度同样延迟的播放，并与 onChange 路径共用去重句柄。

## 可选检查

- 从列表非首项进入，核对标题与播放项和点击项一致。

## 来源（按需复核）

- [case-fe6ca54f30a78eb885f3](../../../store/cases/case-fe6ca54f30a78eb885f3/2da2d9466d0e035a3ff7fe827f6a82b3a09a0da8562ebc78f67fae673e604bc0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`2da2d9466d0e035a3ff7fe827f6a82b3a09a0da8562ebc78f67fae673e604bc0`
