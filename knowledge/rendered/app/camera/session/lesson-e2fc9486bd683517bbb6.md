# 选拍照 profile 时不把字节通路的格式假设写成打开相机的硬门槛：JPEG 优先、接受 RGBA_8888，非 JPEG 走资产通路

## 何时使用

相机实现与返修阶段，为探测会话与正式会话选择拍照 profile、填写拍照尺寸能力，或收窄设备能力过滤时（尤其无法上设备验证时）

## 适用情境

目标从 getSupportedOutputCapability 的 photoProfiles 选拍照输出，拍照字节通路按 photoAvailable 回调里 getComponent(JPEG) 取数据；运行设备或模拟器可能只报告 RGBA_8888 拍照 profile；CameraFormat 枚举还含 YUV、DNG 等值。

## 原因

把下游只取 JPEG 的实现假设前推成 profile 过滤，并在没有 JPEG 时抛错，只报 RGBA 的设备会在探测阶段就释放会话、预览黑屏；宿主 mock 只给 JPEG profile 时测不出来。能力枚举里出现 DNG 格式，也不等于设备支持 RAW 拍摄。

## 做法

1. 收窄 profile 格式过滤前，先在目标设备或模拟器打印 photoProfiles 的 format/size；拿不到设备时保持格式无关的选择，或 JPEG 优先、RGBA_8888 兜底，不在打开相机或探测会话中因缺某种格式抛错。
2. 字节通路只处理 JPEG 时，为选中的非 JPEG profile 安排对应通路（如 photoAssetAvailable 资产通路）；能力枚举只排除确实无法处理的格式，尺寸按宽高去重；RAW 能力不以 DNG 格式出现为依据。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕卡里所用的 API 24 模拟器上，拍照能力 photoProfiles 只报告 RGBA_8888 格式，没有 JPEG
- 〔做法第 2 步〕PhotoOutput.on('photoAssetAvailable') 交付的是媒体库 PhotoAsset，不是带 main 图像、可取 JPEG 组件的 Photo
- 〔做法第 2 步〕MediaAssetChangeRequest.saveCameraPhoto 在非 YUV 拍摄模式下按 CameraFormat 的编码格式保存照片；YUV 模式下保存为默认的 jpg，API 13 起带 ImageFileType 的重载可指定编码格式
