# MediaRecorder 录制器映射成 AVRecorder

agent 会看到什么：读到源端用 MediaRecorder 录音录像（setMaxDuration / setMaxFileSize、OnInfoListener.onInfo 按 what 分支、同步的 stop() / release() 后再重连相机）；规格映射表写「MediaRecorder → AVRecorder 状态机等价」，缺限额行、onInfo 各分支的 AC 或停录与关相机的串行契约

## 规矩

- rule-517ee790d10f｜目标录制器缺原生限额时，映射表登记替代方式及其暂停、停止语义｜读到：源端调 MediaRecorder.setMaxDuration / setMaxFileSize，由录制器自己计时、停止并回调 onInfo；写错：规格映射表没有 setMaxDuration、setMaxFileSize 的行，只把 MEDIA_RECORDER_INFO_* 的语义交给实现层
- rule-620ea75d0d94｜抽取 onInfo 这类多分支事件处理时，每个 what 分支都写验收或写明跳过理由｜读到：源端 MediaRecorder.OnInfoListener 的 onInfo(mr, what, extra) 按 what 分 MAX_DURATION_REACHED、MAX_FILESIZE_REACHED、APPROACHING、NEXT_OUTPUT_FILE_STARTED，并再按是否自动重启分支；写错：规格只为部分分支写了 AC，缺「未开启自动重启时到达文件上限即停止」，或写成「到达上限走某条重启 AC」
- rule-aa8d58c6d2ff｜规格把同步停录、关相机映射到 AVRecorder/CameraKit 时，写 Promise 签名和串行化契约｜读到：源端 MediaRecorder.stop() / release() 同步完成并置空录制器，再重连相机；相机在后台线程阻塞 stopPreview + release 后才置为已关闭；写错：规格接口表写 stopRecording(...): void、release(): void，映射表写「MediaRecorder → AVRecorder 状态机等价·低风险」，没写重复停止、准备期间停止、关相机等停录、拆输出与释放录制器的先后
