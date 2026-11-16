# 相机预览的 TextureView 和 XComponent

agent 会看到什么：读到源端 TextureView 子类重写 onMeasure 按预览比例测量、用 setTransform(matrix) 留边或缩放；产物里预览 XComponent 的 setXComponentSurfaceRect、onAreaChange 和只记进字段的 scale / offset

## 规矩

- rule-e7250d98dabc｜TextureView 的测量和变换落成 setXComponentSurfaceRect 和尺寸变化回调｜读到：源端 `TextureView` 子类重写 `onMeasure` 按预览比例调 `super.onMeasure`，并用 `setTransform(matrix)` 做 4:3 留边或缩放；写错：目标端的变换方法只把 scale/offset 记进字段（注释说是单测口径），没有调用 `setXComponentSurfaceRect`；预览 `XComponent` 只注册 `onLoad`/`onDestroy`、宽高 100%，没有 `onAreaChange` 上报尺寸变化
