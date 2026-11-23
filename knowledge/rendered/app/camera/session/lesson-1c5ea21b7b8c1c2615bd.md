# CameraKit 会话先加齐输入与预览、拍照（录像时加视频）输出再 commitConfig，不提交仅含输入的会话、不在运行中惰性挂输出

## 何时使用

相机功能实现与跨文件接线阶段，为 CameraKit PhotoSession/VideoSession 确定输入输出组合、提交时机、录像档位与录像中拍照入口时（源端在创建会话时一次传入全部输出 surface）

## 适用情境

源端 Camera2 createCaptureSession 一次传入预览 surface、拍照 ImageReader 及录像时的录制 surface；目标用 beginConfig → addInput/addOutput → commitConfig → start 配置会话，用 AVRecorder 的输入 surface 建 VideoOutput；开流前要读取能力，或拍照与录像切换要重建会话；源端按硬件等级推出“录像中拍照”一类能力位。

## 例外与边界

- “加齐”以源端该状态的 surfaces 清单为准：源端会话只有预览（如只取景、扫码不拍照），或录像态只在设备支持录像中拍照时才带拍照 surface 的，目标照源端配，不额外加拍照输出。

## 原因

会话的输出组合在 commitConfig 时确定：只含输入的会话提交失败或无法出流，拍照时再 addOutput 等于重配运行中的会话。录像会话的预览与视频档取自拍照模式能力、只比尺寸并回落首项，会选出与录制不匹配的档位；不调用 videoOutput.start() 录像通道没有数据。录像会话里移除了照片输出，能力位却仍按硬件等级为真，录像中拍照的门控与界面就与会话实际不符。

## 做法

1. 按源端 surfaces 清单，在同一次 beginConfig 中 addInput 并 addOutput 预览与拍照输出（录像态再加 VideoOutput），加齐后 commitConfig、再 start；开流前要取能力时，用带输出的探测会话或 CameraManager.getSupportedOutputCapability，不提交只含输入的会话，也不在拍照时惰性 addOutput。
2. 录像会话的预览档与视频档都取自 NORMAL_VIDEO 模式的能力，按尺寸加帧率范围匹配源端选档；无匹配时返回失败，不回落 profiles[0]。顺序为 commitConfig → session.start → setFrameRate 后 await videoOutput.start() → AVRecorder.start；VideoProfile 的帧率随尺寸一并传到挂接接口。
3. 录像中拍照：NORMAL_VIDEO 能力含 photoProfiles 且 canAddOutput 接受时，才在录像会话中加并发 PhotoOutput，加不上则释放它、继续录像；能力位与按钮门控查询会话实际挂上的 PhotoOutput，不沿用源端按硬件等级推出的常量。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、3 步〕Session.addOutput 与 canAddOutput 只在 Session.addInput 之后、commitConfig 之前有效
- 〔做法第 1、2 步〕CameraManager.getSupportedOutputCapability(camera, mode) 在 CameraManager 上按相机设备和场景模式查询输出能力
- 〔适用情境〕安卓 createCaptureSession 通过传入目标输出 Surface 集合创建会话，这组 Surface 就是会话可用的输出
- 〔做法第 2 步〕VideoProfile.frameRateRange 的帧率单位是 fps
- 〔原因 / 做法第 2 步〕VideoOutput.start 在会话未配置时抛 7400103
- 〔做法第 2 步〕录像时先通过 videoOutput.start 启动录像输出流，再通过 avRecorder.start 开始录像
