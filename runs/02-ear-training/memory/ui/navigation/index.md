# ui/navigation

多屏拆成多页面后的导航挂载与生命周期归属（资源清理、返回刷新）

[上一级](../index.md)

## 本级经验

- [源端一个 Composable 内多屏共享的清理，拆成多页面后归属外层生命周期，切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md)
  - 时机：规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时
  - 情境：源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。
  - 例外：源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理
