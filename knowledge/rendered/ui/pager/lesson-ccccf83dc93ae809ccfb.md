# 分页容器的初始页用 Swiper.index 状态绑定，不在 onReady 里立即调用 changeIndex

## 何时使用

界面实现阶段，把源端 ViewPager 的初始定位（post 里 setCurrentItem）与首播触发转写成 ArkUI Swiper 时

## 适用情境

源端装好数据后在 view.post 等延后回调里 setCurrentItem(index, false)，并靠 onPageSelected 启动当前页；目标在 NavDestination.onReady 读路由参数，Swiper 位于按列表非空条件渲染的分支里。这条只管进入页面时的初始定位：Swiper 挂载之后由用户操作、按钮或回调触发的 changeIndex、showNext 等控制器调用照常有效，保留不动。

## 原因

在 onReady 同一回调里先给列表赋值、再立即调用 SwiperController.changeIndex 时，Swiper 还没挂载，命令被静默丢弃，始终停在第 0 页；源端 post 的延后语义没有落实。

## 做法

1. 路由参数先写入响应式状态，再用 Swiper.index(state) 声明式绑定初始页。
2. 转写 post、doOnLayout 等延后回调时，写明回调执行时哪个组件必须已挂载；容器依赖同一回调里刚赋值的数据才会创建时，它的 controller 此时尚未生效。
3. 源端首播依赖选页回调时，目标对初始项显式调度同样延迟的播放，并与 onChange 路径共用去重句柄。

## 可选检查

- 从列表非首项进入，核对标题与播放项和点击项一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Swiper 的 index 不设时为 0；设置的值小于 0 或大于最大页面索引时取 0
- 〔原因 / 做法第 2 步〕在 NavDestination.onReady 的同一回调里先给列表赋值、再立即调用 SwiperController.changeIndex 时（Swiper 位于按列表非空条件渲染的分支里，此时尚未挂载），调用没有效果，Swiper 始终停在第 0 页；文档没有写明这一行为
- 〔做法第 3 步〕Swiper 的 onChange 在当前显示元素索引变化时触发；动画引起的变化在动画结束时才回调（onSelected 在选中状态改变时立即触发）
