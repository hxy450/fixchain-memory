# 源端 getter 读打开期缓存或逐帧回调写入的相机元数据时，目标改为提交后快照或事件订阅缓存，不在 getter 里调同步相机服务接口

## 何时使用

相机控制器实现阶段，为源端能力枚举 getter 与 capture result 字段（ISO、曝光时间）确定目标取值通道，或在 UI 访问器、定时绘制中消费控制器值时

## 适用情境

源端打开时缓存 CameraCharacteristics 派生的能力，或由 onCaptureCompleted 写入 capture_result_* 字段，调用方在 UI 访问、定时绘制或会话切换中高频读取；目标对应接口（getSupportedOutputCapability、session.isFocusModeSupported/getSupportedIsoRange、getIso/getExposureDuration）是同步相机服务调用，另有 ISO/曝光信息变化事件可订阅。

## 例外与边界

- 逐帧结果的事件有版本条件：拍照会话的 onIsoInfoChange、onExposureInfoChange 自 API 24 起，录像会话的 onIsoInfoChange 自 API 22 起。运行设备上没有对应事件时，这一项按“未就绪”处理（返回源端字段未写入时的值），不退回到在 getter、定时器或绘制回调里同步调用 getIso/getExposureDuration。

## 原因

把读内存字段直译成每次调用同步相机服务接口，调用成本从零变成跨进程往返，结果还随调用时刻的会话状态变化；被定时绘制调用时会卡住主线程。只按 getter 名在 SDK 中检索，找到的是同步查询，而源端数据来自回调。

## 做法

1. 先打开源端字段的赋值点（打开时读一次，还是 onCaptureCompleted 等回调逐帧写入），再在目标 SDK 找同一来源：能力在初次会话 commitConfig 后读一次快照，显示尺寸、zoom 等派生值在内存更新，未就绪时明确报错；逐帧结果订阅会话的 ISO/曝光信息变化事件（onIsoInfoChange/onExposureInfoChange 一类）写缓存，会话停止、替换或暂停时清空。
2. 公开 getter 只读内存；UI 访问器、定时器或绘制回调消费控制器值前，看 getter 实现是否含 session./manager. 的同步调用，含则改读缓存。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕FocusQuery.isFocusModeSupported、AutoExposureQuery.getExposureBiasRange 这类会话能力查询在会话未配置时抛 7400103（只在会话上使用时抛）
- 〔适用情境〕安卓 CaptureCallback.onCaptureCompleted 在一次拍摄完整结束、全部结果元数据可用时回调，之后不会再有该拍摄的部分结果
- 〔做法第 1 步〕onExposureInfoChange 在曝光参数更改后回调更新后的 ExposureInfo，exposureTime 单位微秒；PhotoSession 上的 onIsoInfoChange、onExposureInfoChange 文档标 API 24 起（超出本机 SDK 的 API 23），本机声明只有 VideoSession.onIsoInfoChange（API 22 起），IsoInfo.iso 可缺省
