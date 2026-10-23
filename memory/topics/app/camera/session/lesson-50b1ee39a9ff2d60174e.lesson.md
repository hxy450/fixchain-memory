# 关闭相机或重建会话时按录像输出、stop、各输出、release、input.close 逐步 await，复用输入先 removeInput

ID：`lesson-50b1ee39a9ff2d60174e` · 版本：1 · 阶段：execute · 主题：[app/camera/session](index.md)

概要：会话拆卸逐步 await，复用输入先 removeInput

信号：`CameraDevice.close`, `CameraCaptureSession.close`, `Session.stop`, `Session.release`, `removeInput`, `CameraInput.close`, `VideoOutput.release`, `PhotoOutput.release`

## 何时使用

相机控制器实现阶段，迁移关闭相机、切换前后摄、拍照与录像会话互切或页面销毁，确定拆卸顺序、完成时机与 CameraInput 复用时

## 适用情境

源端在后台线程阻塞执行停止预览与释放，完成后才把状态置为已关闭、回调或重开，销毁时等待关闭任务；目标 CameraInput.close、Session.stop/release、各输出 release 都返回 Promise，重建会话时同一个 CameraInput 要加进新会话。

## 原因

只发起调用不等待，状态在相机真正释放前就变为已关闭，紧接的重开与仍在释放的旧会话竞争。Session.release 会连带关闭仍挂在该会话上的 CameraInput（d.ts 只写“Release capture session instance.”，由设备日志确认），随后把这个 input 加进新会话，预览无法启动。

## 做法

1. 拆卸方法返回 Promise，按“录像输出 → session.stop → 各 output.release → session.release → input.close”逐步 await；已关闭状态、关闭回调与重开只放在 await 完成之后，不用 Promise.resolve().then 包裹不等待的调用来冒充后台任务。
2. 要把同一个 CameraInput 留给下一会话时，按 stop → beginConfig → removeInput(input) → release 处理旧会话；removeInput 只在 beginConfig 与 commitConfig 之间有效（API 24 camera.d.ts L4765–L4776）。
3. 关闭进行中收到打开或恢复请求时记为待重开，关闭完成后再执行，不直接丢弃；页面销毁与 onDestroy 走同一条有序关闭路径（等待完成或沿用源端等待上限），不另写同步强释放。

## 可选检查

- 宿主单测的 session mock 在 release 时关闭仍挂载的 input，用来覆盖会话重建路径

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [会话一次配齐输出再提交，拍照档不硬限 JPEG](lesson-05cd365740c0003662a4.lesson.md)（共享 1 张卡）
- [阻塞等待改 Promise 后签名与调用链一路 await](../../../arkts/async-mapping/lesson-c53d56284f178b5ab63f.lesson.md)（共享 1 张卡）
- [AVRecorder 启停串行：共享停止任务、启动可取消](../recording/lesson-d41878bcc79f7e356a54.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-9284c0c57d1d9b75b702](../../../../../store/cases/case-9284c0c57d1d9b75b702/d6b77b5d9b22e4a3275477c938a537518211a577b165c7880850d1f42393acd6.json) · 结论：diagnosis, rec-1044537ed6
  卡片版本：`d6b77b5d9b22e4a3275477c938a537518211a577b165c7880850d1f42393acd6`
- [case-b89cd099bfa87829fd2d](../../../../../store/cases/case-b89cd099bfa87829fd2d/063e8bf906db6adb5fae0a419989e043b3d8f5f8f5679ae18a2371e50e26fb54.json) · 结论：diagnosis, rec-4704c8c596, rec-1ab9c09711
  卡片版本：`063e8bf906db6adb5fae0a419989e043b3d8f5f8f5679ae18a2371e50e26fb54`
