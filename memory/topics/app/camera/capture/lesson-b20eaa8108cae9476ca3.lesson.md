# 源端前摄以屏幕补光代替闪光、由控制器在预拍阶段回调界面时，目标控制器保留补光判定与触发出口，编排器拍前触发并按回退时序等待

ID：`lesson-b20eaa8108cae9476ca3` · 版本：1 · 阶段：execute/repair · 主题：[app/camera/capture](index.md)

概要：前屏补光保留控制器判定出口与回退等待

信号：`CONTROL_AE_PRECAPTURE_TRIGGER`, `CONTROL_AE_STATE`, `LENS_FACING_FRONT`, `FLASH_MODE_CLOSE`, `screenBrightness`, `setWindowBrightness`

## 何时使用

相机控制器、拍照编排与页面 VM 实现及返修阶段，迁移前摄屏幕补光的触发、自动判定、提亮与白色覆盖层和结束复位时

## 适用情境

源端控制器在预拍阶段（Camera2 依 AE 状态的预拍流程，或旧相机 API 路径的定时回退）回调界面打开前屏补光，自动模式按当前 ISO 阈值判定，界面提亮窗口并在预览上画全屏白层，相机操作结束时复位；目标把控制器、拍照编排器、页面 VM 与覆盖层拆到不同切片，CameraKit 公开接口没有 AE 状态事件（API 24 camera.d.ts 无 ExposureState 或曝光状态事件）。

## 原因

补光显示交给界面后，控制器的判定与回调出口、编排器的触发、VM 的白层转发分属不同切片，任一处只做自己可见的部分（硬件闪光设为 CLOSE 并注释“由界面承担”、只提亮不画白层），整条链就不会触发。目标没有 AE 状态事件，沿用 AE 驱动的时序也等不到触发点。

## 做法

1. 控制器把硬件闪光设为 FLASH_MODE_CLOSE 的同时，保留“是否需要前屏补光”查询（前摄、开启或自动且当前 ISO 达到源端阈值）与触发出口；跨切片延后时登记占位并写明消费方。
2. 拍照编排在拍照前调用触发出口，按源端无 AE 状态路径的回退时序（读源端旧 API 路径的等待时长）等待后再拍，并在规格里标注与 AE 驱动时序的差异。
3. VM 或门面转发源端补光接口的全部动作（提亮与白层），完成、失败、取消、进入后台、拍后暂停预览等所有结束路径都复位亮度与白层；拍后暂停预览分支只复位补光，不调用会恢复普通拍摄界面的“相机操作结束”接口，对照源端该分支实际调用的接口。
4. 新增取消补光等待的路径时复用已有的作废机制（如拍照代数递增），同时作废已登记的对焦续体，避免取消后迟到的回调仍然拍照。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [必读 skill 与源码逐份读全，截断即重读再写码](../../../process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [拆层后各层方法按源端覆写与调用全集核对](../../../process/enumeration-gaps/lesson-61a9fc7190c51c663697.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-7aad6dd3649e8ed51a17](../../../../../store/cases/case-7aad6dd3649e8ed51a17/698a09982d97a56c5d6e5616d835be92d2ad703bf9dd02dbaa4cc04bdac4e0dc.json) · 结论：diagnosis, rec-3f02cc1aab, rec-c2322d02f7, rec-fb6607aed7, rec-63bda677ae, rec-967c73449f
  卡片版本：`698a09982d97a56c5d6e5616d835be92d2ad703bf9dd02dbaa4cc04bdac4e0dc`
