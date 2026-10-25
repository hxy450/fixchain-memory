# app/camera/session

相机会话：提交前配齐输入与输出、录像档位与帧率、拆卸与重建时 CameraInput 的复用、拍照 profile 格式选择、能力位按会话查询填写、能力与逐帧元数据的快照或事件缓存

[上一级](../index.md)

## 本级经验

- [CameraKit 会话先加齐输入与预览、拍照（录像时加视频）输出再 commitConfig，不提交仅含输入的会话、不在运行中惰性挂输出](lesson-1c5ea21b7b8c1c2615bd.lesson.md)
  - 时机：相机功能实现与跨文件接线阶段，为 CameraKit PhotoSession/VideoSession 确定输入输出组合、提交时机、录像档位与录像中拍照入口时
  - 情境：源端 Camera2 createCaptureSession 一次传入预览 surface、拍照 ImageReader 及录像时的录制 surface；目标用 beginConfig → addInput/addOutput → commitConfig → start 配置会话，用 AVRecorder 的输入 surface 建 VideoOutput；开流前要读取能力，或拍照与录像切换要重建会话；源端按硬件等级推出“录像中拍照”一类能力位。
- [源端 getter 读打开期缓存或逐帧回调写入的相机元数据时，目标改为提交后快照或事件订阅缓存，不在 getter 里调同步相机服务接口](lesson-2fd3f5f24a7571d3eded.lesson.md)
  - 时机：相机控制器实现阶段，为源端能力枚举 getter 与 capture result 字段（ISO、曝光时间）确定目标取值通道，或在 UI 访问器、定时绘制中消费控制器值时
  - 情境：源端打开时缓存 CameraCharacteristics 派生的能力，或由 onCaptureCompleted 写入 capture_result_* 字段，调用方在 UI 访问、定时绘制或会话切换中高频读取；目标对应接口（getSupportedOutputCapability、session.isFocusModeSupported/getSupportedIsoRange、getIso/getExposureDuration）是同步相机服务调用，另有 ISO/曝光信息变化事件可订阅。
- [相机能力位与可选值按已提交会话的 isXxxSupported/getXxxRange 查询填写，SDK 声明了枚举或 setter 不等于支持](lesson-1c175988beebe0d7c4dc.lesson.md)
  - 时机：相机能力探测实现阶段，为曝光/白平衡锁、色温、白平衡预设、录像中拍照、RAW 等支持位与可选值列表填值时；规格提取阶段把源端能力位规则写进目标契约时
  - 情境：源端能力位来自 Camera2 CameraCharacteristics（可用 AE/AWB 模式、硬件等级、RAW_SENSOR 输出尺寸），或由源码硬编码为常量；目标 @ohos.multimedia.camera 的 d.ts 里可见 ExposureMode、WhiteBalanceMode 的 LOCKED、MANUAL 等枚举与对应 setter，会话接口以 interface Xxx extends XxxQuery 分出查询方法；规格可能给出条件式能力规则（多个条件缺一即 false、按硬件等级、尺寸只列 JPEG），也可能把源端常量写成“恒为 true”。
- [选拍照 profile 时不把字节通路的格式假设写成打开相机的硬门槛：JPEG 优先、接受 RGBA_8888，非 JPEG 走资产通路](lesson-e2fc9486bd683517bbb6.lesson.md)
  - 时机：相机实现与返修阶段，为探测会话与正式会话选择拍照 profile、填写拍照尺寸能力，或收窄设备能力过滤时（尤其无法上设备验证时）
  - 情境：目标从 getSupportedOutputCapability 的 photoProfiles 选拍照输出，拍照字节通路按 photoAvailable 回调里 getComponent(JPEG) 取数据；运行设备或模拟器可能只报告 RGBA_8888 拍照 profile；CameraFormat 枚举还含 YUV、DNG 等值。
- [释放或重建 CameraKit 会话时逐步 await 拆卸；要复用的 CameraInput 先 removeInput 再 release 旧会话](lesson-1368f3a5be74739ee346.lesson.md)
  - 时机：相机实现与返修阶段，编写会话关闭、拍照与录像会话切换、探测会话转正式会话的拆卸代码时
  - 情境：拍照/录像切换或探测会话转正式会话需要重建 CameraKit 会话并复用同一个 CameraInput；源端 Camera2 在后台线程按顺序同步停止预览、关闭会话与设备；目标 session.stop/release、各 output 的 release、cameraInput.close 都返回 Promise。
