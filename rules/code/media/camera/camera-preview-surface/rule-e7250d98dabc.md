# TextureView 的测量和变换落成 setXComponentSurfaceRect 和尺寸变化回调

审的是：代码
触发（任一种）：
- 读到：源端 `TextureView` 子类重写 `onMeasure` 按预览比例调 `super.onMeasure`，并用 `setTransform(matrix)` 做 4:3 留边或缩放；写错的样子：目标端的变换方法只把 scale/offset 记进字段（注释说是单测口径），没有调用 `setXComponentSurfaceRect`；预览 `XComponent` 只注册 `onLoad`/`onDestroy`、宽高 100%，没有 `onAreaChange` 上报尺寸变化
适用范围：把安卓相机预览的 TextureView 测量和矩阵变换迁到 ArkUI XComponent（SURFACE 或 TEXTURE 类型）时
做法：
- 按测量结果算出 surface 矩形，调用 `xComponentController.setXComponentSurfaceRect({ offsetX, offsetY, surfaceWidth, surfaceHeight })` 让预览居中，四个值都是 px
- 在预览 XComponent 上接 `.onAreaChange((oldValue, newValue) => …)`，把新宽高经 `vp2px` 换成 px 交给预览引擎，尺寸变化时重算并重设 surface 矩形
- 验收条目里断言矩阵参数只是检查口径，测量和变换必须落成真实调用，不能只记录参数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setXComponentSurfaceRect(rect: SurfaceRect): void：设置 XComponent 持有的 surface 的矩形（声明 @since 12）（出处：鸿蒙 SDK 的 ets/component/xcomponent.d.ts，XComponentController.setXComponentSurfaceRect）
- SurfaceRect { offsetX?: number; offsetY?: number; surfaceWidth: number; surfaceHeight: number }，单位 px；offsetX/offsetY 不写时 surface 在该轴上居中：矩形参数：偏移相对 XComponent 左上角（出处：鸿蒙 SDK 的 ets/component/xcomponent.d.ts，SurfaceRect）
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件尺寸或位置变化完成后回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 改成按测量结果调 setXComponentSurfaceRect 居中，并接上 onAreaChange → 尺寸变化（vp2px 换算）后预览居中正确：修好后的写法（出处：卡里修好并验证过）
- getXComponentSurfaceRect(): SurfaceRect：同族接口：读回当前 surface 矩形（出处：鸿蒙 SDK 的 ets/component/xcomponent.d.ts，XComponentController.getXComponentSurfaceRect）
- onSurfaceChanged(surfaceId: string, rect: SurfaceRect): void：同族接口：surface 矩形变化后的回调（出处：鸿蒙 SDK 的 ets/component/xcomponent.d.ts，XComponentController.onSurfaceChanged）
未核实：卡里的行为出自鸿蒙 SDK API 24（6.1.1），本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-ef167da8e80990c31714（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 1；取值 4 ← 诊断
