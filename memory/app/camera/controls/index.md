# app/camera/controls

取景控制：手动曝光、曝光补偿、ISO、对焦的单位、值域与前置条件，预览 surface 的缩放居中、传感器朝向与拍照旋转

[上一级](../index.md)

## 本级经验

- [Camera2 手动曝光、ISO、对焦迁到 CameraKit 时按 d.ts 注释换单位与值域，能力读回与设定下发对称换算](lesson-f260fb566ed3ae1d0dd4.lesson.md)
  - 时机：相机控制器实现与规格提取阶段，把源端 Camera2 的曝光时长、曝光补偿、ISO 与对焦距离的能力范围和设定映射到 CameraKit 会话接口时
  - 情境：源端能力结构以 ns 记曝光时长、以整数档位加步长记曝光补偿、以上下限记 ISO、以屈光度记对焦距离（0 为无限远）；目标使用 HarmonyOS CameraKit 的 ManualExposure、AutoExposure、ManualIso、ManualFocus 接口，查 d.ts 时 grep 可能只返回方法签名、过滤掉方法上方的注释。
- [相机预览居中与拍照旋转落成真实调用：surface 用 setXComponentSurfaceRect，拍照用 getPhotoRotation](lesson-33cc1f6be3e707c17241.lesson.md)
  - 时机：相机功能实现阶段，把 Android 预览的测量与矩阵变换、传感器朝向和拍照前的旋转下发移植到 XComponent 与 CameraKit 时
  - 情境：源端 TextureView 子类在 onMeasure 按预览比例测量、setTransform 应用矩阵做 letterbox 与居中，尺寸变化时重配；拍照前 setRotation(getImageVideoRotation()) 写 JPEG_ORIENTATION（已含传感器角）；传感器角取 SENSOR_ORIENTATION。目标预览是 XComponent(SURFACE)，拍照经 PhotoOutput.capture(PhotoCaptureSetting)；规格验收可能把矩阵参数断言列为单测口径。
