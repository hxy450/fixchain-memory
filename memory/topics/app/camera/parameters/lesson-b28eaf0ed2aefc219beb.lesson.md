# 为 CameraKit 填写曝光锁、白平衡、色温、录像中拍照、RAW 等能力位时，按会话与模式查询并在提交后快照一次，SDK 有枚举或 setter 不算支持

ID：`lesson-b28eaf0ed2aefc219beb` · 版本：1 · 阶段：spec/execute · 主题：[app/camera/parameters](index.md)

概要：能力位按会话查询并在提交后快照

信号：`CameraCharacteristics`, `CONTROL_AWB_AVAILABLE_MODES`, `isExposureModeSupported`, `isWhiteBalanceModeSupported`, `getWhiteBalanceRange`, `WhiteBalanceQuery`, `getSupportedOutputCapability`, `photoProfiles`, `CAMERA_FORMAT_DNG`, `DngCreator`, `NORMAL_VIDEO`

## 何时使用

规格提取与相机控制器实现阶段，把源端由 CameraCharacteristics 推出或源码硬编码的能力位写成目标契约、填写能力对象的各支持位与白平衡可选值，并决定能力 getter 的取值时机时

## 适用情境

源端能力位来自 CameraCharacteristics（AWB 可用模式、硬件等级、RAW_SENSOR 尺寸）或被源码直接写成 true，打开相机时取一次，之后由高频 getter 读字段；目标的支持查询（isExposureModeSupported、isWhiteBalanceModeSupported、getWhiteBalanceRange、各模式 photoProfiles）是同步相机服务调用，多数要在已提交的会话上执行；SDK 的 ExposureMode、WhiteBalanceMode、CameraFormat 含 LOCKED、MANUAL、DNG 等成员。

## 原因

枚举成员与 setter 只说明 API 形态，不说明当前设备与模式支持；据此把锁、色温、录像中拍照、RAW 报成可用，界面开放后设定无效或保存出伪文件。源端硬编码 true 是源端的设备假设，照抄成目标契约同样跳过了查询。能力 getter 每次重新查询会话，又把打开期一次性数据变成反复的同步相机服务调用，结果还随调用时的会话状态变化。

## 做法

1. 每个支持位先找到目标查询再写：曝光锁 isExposureModeSupported(EXPOSURE_MODE_LOCKED)；白平衡锁 isWhiteBalanceModeSupported(LOCKED)；色温 isWhiteBalanceModeSupported(MANUAL) 且范围取 getWhiteBalanceRange()；录像中拍照看 NORMAL_VIDEO 模式的 photoProfiles 是否有可处理格式。遇到 interface X extends XQuery 时先展开 Query 接口找 isXxxSupported/getXxxRange（camera.d.ts L3682 起）。
2. 白平衡可选值按 WhiteBalanceMode 逐个查询后暴露；解锁时恢复用户所选的模式与色温，不固定回 AUTO。
3. 规格给出条件式能力（多条件同时成立、按硬件等级、只列 JPEG 尺寸）时逐条找目标等价查询；找不到就置 false 并登记差异，不改写成常量 true 或固定范围。源码硬编码的能力位写进契约时注明“源端常量，目标按会话查询”，并给出查询 API。
4. CAMERA_FORMAT_DNG profile 存在不等于能产出 DNG 文件：工程没有 DNG 封装（源端 DngCreator 的写出等价物）时，RAW 支持位置 false、图片尺寸只列可处理格式的 profile，RAW 保存在创建媒体资产之前返回失败并提示，不把原始缓冲按 .dng 落盘并报成功。
5. 能力在初次拍照会话 commitConfig 后读取一次形成快照，显示尺寸、zoom 等派生值在内存更新；公开 getter 与界面访问器只读快照，未就绪时明确报错，不返回部分结果，也不在访问器里直接触发 session. 或 manager. 查询。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [实时 ISO/曝光/振幅经事件或单飞采样入缓存](lesson-221830205a3dff3cb74b.lesson.md)（共享 1 张卡）
- [占位只登记输入缺值的情况，能实现的当场实现](../../../process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md)（共享 1 张卡）
- [规格常量分应用参数与源平台取值，后者写目标取法](../../../process/unverified-as-fact/lesson-d280d90bb76be18536f6.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-168300edfa3644b0f14a](../../../../../store/cases/case-168300edfa3644b0f14a/79e3a447504de5357a4bc6ac0687a348e9214a503b0e3ef26e892f4d596ce8b3.json) · 结论：diagnosis, rec-cc874a92ba, rec-9c35215091, rec-68e43a7a34, rec-5b92fc969b
  卡片版本：`79e3a447504de5357a4bc6ac0687a348e9214a503b0e3ef26e892f4d596ce8b3`
- [case-d160173a312daca7fc69](../../../../../store/cases/case-d160173a312daca7fc69/d91c39d7295c87d4a04f83610561ebe0ef66c0dfd3d09f47323efc62976d0f41.json) · 结论：diagnosis, rec-91bc99d42d, rec-dfa209ff09, rec-748a3d3624
  卡片版本：`d91c39d7295c87d4a04f83610561ebe0ef66c0dfd3d09f47323efc62976d0f41`
