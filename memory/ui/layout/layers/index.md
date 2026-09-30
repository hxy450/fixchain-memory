# ui/layout/layers

运行时addView挂载、全屏底层与状态覆盖层，以及动效/气泡锚点的坐标与取值时机。

[上一级](../index.md)

## 本级经验

- [为已转换页面接线时保留“全屏底层 + 按状态切换的前景层”骨架；地图 SDK 不可用也不把全屏承载改成自绘小卡](lesson-4de4283ec625be7e976c.lesson.md)
  - 时机：功能切片为已转换页面接入 ViewModel、Service 与跳转，决定保留还是重写布局骨架时；巡检修复处理“缺少全屏地图承载”一类发现时
  - 情境：Android 页面以全屏 MapView/导航视图为底层，前景由 ViewModel 布尔状态（如 showRoute）切换两套覆盖层；导航页 FEATURE_NO_TITLE、只承载导航视图；目标地图/导航 SDK 暂不可用，页面转换阶段已写出带全屏占位底图与两态覆盖层的骨架。
- [播放器面等运行时 addView 挂到根部的层，按运行时层级实现，不按 XML 里的占位区域定几何](lesson-c3dcc5a25a0ad59c53c1.lesson.md)
  - 时机：界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时
  - 情境：源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0) 无约束铺满），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。
- [源端在触发瞬间读取锚点窗口位置时，目标在点击回调里取本次手势坐标或即时查询，onAreaChange 缓存只作兜底；锚点取源端传入的同一元素](lesson-963bf871aa4e910a8fc8.lesson.md)
  - 时机：界面实现与修复阶段，为从点击处发出的动效或气泡（完成彩纸、锚点提示）确定起点坐标与锚点元素时
  - 情境：源端在动效或弹窗被调用时用 getLocationInWindow 读取传入锚点 View 的当下窗口中心；目标列表项存在 translate 平移、LazyForEach/Repeat 节点复用或弹层内滚动，写者准备用 onAreaChange 缓存控件位置。
